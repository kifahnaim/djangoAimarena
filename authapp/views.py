from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Userreg
from django.contrib import messages
from .forms import LoginForm, RegistrationForm
from django.core.exceptions import ObjectDoesNotExist


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
    if request.method == "POST":
        try:

            Userdetails = Userreg.objects.get(Username=request.POST.get('Username'),
                                              password=request.POST.get('password'))

            print("Username", Userdetails)

            if Userdetails is not None:
                request.session["Username"] = Userdetails.Username
                request.session["Useremail"] = Userdetails.Useremail
                request.session["userid"] = Userdetails.id
                request.session["Role"] = Userdetails.Role_id
                print(request.session["Role"])

                if request.GET.get('next', None):
                    if request.session.get('Username'):
                        valuenext = request.POST.get('next')
                        print("kifah naim " + valuenext)

                        return HttpResponseRedirect('../../forum')
                else:
                    return render(request, 'home.html')
            else:
                print("No user")


        except ObjectDoesNotExist:

            print("fail")

    return render(request, 'signin.html')


def Userregistration(request):
    if request.method == "POST":
        context = {}
        if request.POST.get("Username") and request.POST.get("Useremail") and request.POST.get(
                "Firstname") and request.POST.get("Lastname") and request.POST.get("password"):
            Usercount = Userreg.objects.filter(Username=request.POST.get("Username")).count()

            try:
                if Usercount < 1:
                    saverecord = Userreg()
                    saverecord.Username = request.POST.get("Username")
                    saverecord.password = request.POST.get("password")
                    saverecord.Firstname = request.POST.get("Firstname")
                    saverecord.Lastname = request.POST.get("Lastname")
                    saverecord.Useremail = request.POST.get("Useremail")
                    saverecord.save()
                    messages.success(request, "New User Registration Details Saved Successfully..!")
                    return redirect('../../auth/signin/')
                else:
                    error = "This username already exists"
                    return render(request, 'signup.html', context)

            except:
                error = "An unexpected error occured"
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
