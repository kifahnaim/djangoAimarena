from datetime import datetime, timedelta
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db import connection
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from passlib.hash import pbkdf2_sha256
from forum.models import Emaillogs
from .utils import account_activation_token
from nonmotiongame.models import User_Info
from .models import Userreg, login_details, admin_actions, UserSession, Banfromforum, Banfromgame
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from humanfriendly import format_timespan


def signin(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['Username']
            password = forms.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    context = {
        'form': forms
    }
    return render(request, 'signin.html', context)


def Userlogin(request):
    kicked = None
    userid = request.session.get('userid')
    if userid:
        return redirect('forums:forum')
    if request.method == "POST":
        try:

            Userdetails = Userreg.objects.get(Username=request.POST.get('Username'))

            print("Username", Userdetails)

            if Userdetails is not None:
                if Userdetails.is_active:
                    if pbkdf2_sha256.verify(request.POST.get('password'), Userdetails.password):
                        request.session["Username"] = Userdetails.Username
                        request.session["Firstname"] = Userdetails.Firstname
                        request.session["Lastname"] = Userdetails.Lastname
                        request.session["Useremail"] = Userdetails.Useremail
                        request.session["userid"] = Userdetails.id
                        request.session["Role"] = Userdetails.Role_id
                        request.session["RoleName"] = Userdetails.Role.RoleName
                        context = {}
                        UserSession.user_logged_in_handler(request=request, customuser=Userreg(Userdetails.id))

                        criterion1 = Q(user_kick_forum=True)
                        criterion2 = Q(user_id_id=Userdetails.id)
                        query = admin_actions.objects.filter(criterion1 & criterion2)
                        if query:
                            print("kicked")
                            print(query)
                            kicked = "You were recently kicked, please behave well!"
                        else:
                            kicked = "nothing"
                        banforum = None
                        bangame = None
                        print(request.session["Role"])
                        checkbanforum = admin_actions.objects.filter(user_ban_forum=True,
                                                                     user_id_id=Userreg(Userdetails.id))
                        checkbangame = admin_actions.objects.filter(user_ban_game=True,
                                                                    user_id_id=Userreg(Userdetails.id))
                        if checkbanforum:
                            banfromforumtable = Banfromforum.objects.filter(user_id_id=Userreg(Userdetails.id))
                            for i in banfromforumtable:
                                now = datetime.now()
                                print(now)
                                print(i.Banned_until)
                                if now < i.Banned_until:
                                    timebanforum = i.Banned_until - now
                                    banforum = "You are banned from the forum for " + str(
                                        format_timespan(i.Banned_until - now))
                                else:
                                    banforum = None
                                    updateforumban = admin_actions.objects.filter(
                                        user_id_id=Userreg(Userdetails.id)).update(
                                        user_ban_forum=False, create_appeal=False)
                        if checkbangame:
                            now = datetime.now()
                            banfromgametable = Banfromgame.objects.filter(user_id_id=Userreg(Userdetails.id))
                            for i in banfromgametable:
                                if now < i.Banned_until:
                                    bangame = "You are banned from the Aim Arena game for " + str(
                                        format_timespan(i.Banned_until - now))
                                else:
                                    updategameban = admin_actions.objects.filter(
                                        user_id_id=Userreg(Userdetails.id)).update(
                                        user_ban_game=False)

                        if request.session.get('RoleName') == "User":
                            print("hello user")
                            if login_details.objects.filter(user_id_id=Userdetails.id).count() < 1:
                                login = login_details()
                                login.lastlogin = datetime.now()
                                login.user_id = Userreg(Userdetails.id)
                                login.save()

                            else:
                                login_details.objects.filter(user_id_id=Userdetails.id).update(lastlogin=datetime.now(),
                                                                                               user_id_id=Userdetails.id)
                            admin_actions.objects.filter(user_id_id=Userreg(Userdetails.id)).update(
                                user_kick_forum=False)

                            return render(request, 'home.html',
                                          {"kicked": kicked, "banforum": banforum, "bangame": bangame,
                                           "role": request.session.get('RoleName')})
                        elif request.session.get('RoleName') == "Admin":
                            return render(request, 'home.html',
                                          {"kicked": kicked, "banforum": banforum, "bangame": bangame,
                                           "role": request.session.get('RoleName')})

                        elif request.session.get('RoleName') == "Forum Moderator":
                            return render(request, 'home.html',
                                          {"kicked": kicked, "banforum": banforum, "bangame": bangame,
                                           "role": request.session.get('RoleName')})

                        elif request.session.get('RoleName') == "Customer Service":
                            return render(request, 'home.html',
                                          {"kicked": kicked, "banforum": banforum, "bangame": bangame,
                                           "role": request.session.get('RoleName')})
                    else:
                        messages.error(request, "Please check your username or password ")
                else:
                    messages.error(request, "Please activate your account ! ")

            else:
                messages.error(request, "Please check your username or password ")


        except ObjectDoesNotExist:
            print("fail")
            messages.error(request, "please try again with a different username or password! ")

    return render(request, 'signin.html')


def Userregistration(request):
    userid = request.session.get('userid')
    if userid:
        return redirect('forums:forum')
    if request.method == "POST":
        context = {}
        print("hello")
        if request.POST.get("Username") and request.POST.get("Useremail") and request.POST.get(
                "Firstname") and request.POST.get("Lastname") and request.POST.get("password"):
            Usercount = Userreg.objects.filter(Username=request.POST.get("Username")).count()
            emailcount = Userreg.objects.filter(Useremail=request.POST.get("Useremail")).count()
            passlength = request.POST.get("password")
            print("hello")
            try:
                print(Usercount)

                if Usercount < 1:
                    if emailcount < 1:
                        if len(passlength) > 6:
                            # hash password
                            encpassword = pbkdf2_sha256.hash(request.POST.get("password"))
                            print(encpassword)
                            saverecord = Userreg()
                            saverecord.Username = request.POST.get("Username")
                            saverecord.password = encpassword
                            saverecord.Firstname = request.POST.get("Firstname")
                            saverecord.Lastname = request.POST.get("Lastname")
                            saverecord.Useremail = request.POST.get("Useremail")

                            saverecord.save()
                            nowregistered = Userreg.objects.filter(Useremail=request.POST.get("Useremail"),
                                                                   Username=request.POST.get("Username"),
                                                                   Firstname=request.POST.get("Firstname"),
                                                                   Lastname=request.POST.get("Lastname"))
                            current_site = get_current_site(request)
                            print(current_site)
                            print(nowregistered[0])
                            email_contents = {
                                'user': nowregistered[0],
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(nowregistered[0].pk)),
                                'token': account_activation_token.make_token(nowregistered[0])

                            }

                            link = reverse('activate',
                                           kwargs={'uidb64': email_contents['uid'], 'token': email_contents['token']})

                            activate_url = 'http://' + current_site.domain + link
                            message_name = 'Activate your account'
                            message_email = request.POST.get("Useremail")
                            message = "Activate your account on Aim Arena by using the link provided below + \n" + activate_url
                            msg = EmailMessage(message_name,
                                               message, to=[message_email])
                            msg.send()
                            return redirect('../../auth/signin/')
                        else:
                            messages.error(request, "Password too short")

                            return render(request, 'signup.html')

                    else:
                        messages.error(request, "This email is already registered on this website")

                        return render(request, 'signup.html')


                else:
                    messages.error(request, "This username already exists")

                    return render(request, 'signup.html')

            except:
                error = "An unexpected error occured"
                print(error)
                context = {"error": error}
                return render(request, 'signup.html', context)


    else:
        return render(request, 'signup.html')


def signup(request):
    forms = RegistrationForm()
    if request.method == 'POST':
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            firstname = forms.cleaned_data['firstname']
            lastname = forms.cleaned_data['lastname']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            confirm_password = forms.cleaned_data['confirm_password']
            if password == confirm_password:
                try:
                    User.objects.create_user(username=username, password=password, email=email, first_name=firstname,
                                             last_name=lastname)
                    return redirect('signin')
                except:
                    context = {
                        'form': forms,
                        'error': 'This Username Already exists!'
                    }
                    return render(request, 'signup.html', context)
    context = {
        'form': forms
    }
    return render(request, 'signup.html', context)


def signout(request):
    logout(request)
    request.session.pop("Username", None)
    return redirect('signin')


def resetpassword(request):
    userid = request.session.get('userid')
    if userid:
        return redirect('forums:forum')
    return render(request, 'resetpass.html')


def resetpasswordsendemail(request):
    if request.method == "POST":
        emailInput = request.POST.get('emailInput')
        emailvalid = Userreg.objects.filter(Useremail=emailInput)
        print('emailvalid')

        if emailvalid:
            current_site = get_current_site(request)

            print(emailvalid[0].pk)
            email_contents = {
                'user': emailvalid[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(emailvalid[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(emailvalid[0])

            }
            print('emailvalid')
            link = reverse('reset-user-password', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})
            print(link)
            reset_url = 'http://' + current_site.domain + link
            message_name = 'Password reset instructions'
            message_email = emailInput
            message = "Hi there, This email is sent for " + str(emailvalid[
                                                                    0].Username) + " to reset the password of his account on AimArena. " + "\n" + "Please press the link below to reset your password." \
                      + "\n" + reset_url
            print(current_site.domain)
            msg = EmailMessage(message_name,
                               message, to=[message_email])
            msg.send()
            sentemail = Emaillogs()
            sentemail.email_message = message
            sentemail.email_type = "Automatic mail forgot password"
            sentemail.email_token = email_contents['token']
            sentemail.email_url = reset_url
            sentemail.user = emailvalid[0]
            sentemail.save()
            return JsonResponse({"message": "success"})
        else:
            messages.error(request, 'Email is not registered on Aim Arena')

    else:
        return JsonResponse({"message": "fail"})


class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = Userreg.objects.get(pk=user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.info(request, 'Password link is invalid, please request a new one')
            return redirect('resetpassword')
        return render(request, 'set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST.get("password")
        password2 = request.POST.get("repwd")
        if len(password) < 6:
            messages.error(request, "Password too short")
            return render(request, 'set-new-password.html', context)
        user_id = force_text(urlsafe_base64_decode(uidb64))
        Userreg.objects.filter(pk=user_id).update(password=pbkdf2_sha256.hash(password))

        return render(request, 'signin.html', context)


def homelogin(request):
    if request.session.get('userid'):
        return render(request, "home.html")
    else:
        return redirect('signin')


class VerificationView(View):
    def get(self, request, uidb64, token):

        try:
            active = False
            id = force_text(urlsafe_base64_decode(uidb64))
            user = Userreg.objects.get(pk=id)
            print(user)

            if not account_activation_token.check_token(user, token):
                print(token)
                messages.error(request, "Already activated")
                return redirect('signin' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('signin')

            user.is_active = True
            messages.info(request, "Your account is now activated, You can sign in now !")
            user.save()

        except Exception as ex:
            pass

        return redirect('signin')