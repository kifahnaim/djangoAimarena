from datetime import datetime

from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from humanfriendly import format_timespan

import nonmotiongame
from authapp.models import Userreg, admin_actions, Banfromgame
from authentication import settings
from home.models import emailnews, unsubscribefeedback, newsbanner

from nonmotiongame.models import GameMode_User





def game(request):
    bangame = None
    Userdetails = None
    subscribed = emailnews.objects.filter(userid=request.session.get("userid")).values('subscription')
    print(subscribed)
    scores = GameMode_User.objects.filter(Game_Mode_ID=1).order_by('-Score_Avg')[0:7]
    numbers = scores.count()
    userid=request.session.get("userid")
    bannernews = newsbanner.objects.filter(is_deleted=0)
    if request.session.get("userid"):
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
        banned = admin_actions.objects.values_list('user_ban_game', flat=True).filter(user_id=request.session.get("userid"))
        banfromforumtable = Banfromgame.objects.filter(user_id_id=request.session.get("userid"))
        for i in banfromforumtable:
            now = datetime.now()
            print(now)
            print(i.Banned_until)
            if now < i.Banned_until:
                timebangame = i.Banned_until - now
                bangame = str(
                    format_timespan(i.Banned_until - now))
        print(banned)
    print("helloworld")
    context = {"leaderboards": scores, "subscribed": subscribed, "bannernews": bannernews,"bangame":bangame, "Userdetails": Userdetails}
    return render(request, "index.html", context)


def terms(request):
    userid=request.session.get("userid")
    Userdetails = None
    if userid:
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    context = {"Userdetails": Userdetails}
    return render(request, "Terms.html", context)

def about(request):
    userid=request.session.get("userid")
    Userdetails = None
    if userid:
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    context = {"Userdetails": Userdetails}
    return render(request, "about.html", context)

def privacy(request):
    userid=request.session.get("userid")
    Userdetails = None
    if userid:
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    context = {"Userdetails": Userdetails}
    return render(request, "privacy.html", context)


def leaderboards(request):
    userid=request.session.get("userid")
    Userdetails = None
    if userid:
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    scores = GameMode_User.objects.filter(Game_Mode_ID=1).order_by('-Score_Avg')
    context = {"leaderboards": scores, "Userdetails":Userdetails}
    return render(request, "leaderboards.html", context)


def contact(request):
    userid=request.session.get("userid")
    Userdetails = None
    if userid:
        Userdetails = Userreg.objects.get(id=userid).user_thumbnail
    return render(request, "contact.html", {"Userdetails": Userdetails})


def contactus(request):
    if request.method == "POST":
        message_email = "aimarenaofficial@gmail.com"
        message = request.POST.get('message')
        message_name = request.POST.get('name')
        emailfrom = request.POST.get('email')
        print(message)
        print(message_name)
        settings.EMAIL_HOST_USER = emailfrom
        print(settings.EMAIL_HOST_USER)
        try:
            send_mail(
                'Aim Arena contact',
                message_name + '\n' + emailfrom + '\n' +
                message,
                settings.EMAIL_HOST_USER,
                [message_email],
                fail_silently=False,
            )
            messages.info(request, "Email sent successfully !")
        except:
            messages.error(request, "An unexpected error has occured, please try again later !")
        return redirect('contact')
    else:
        return redirect('contact')


def emaillist(request):
    if request.method == "POST":
        email = request.POST.get("emailnews")
        count = Userreg.objects.filter(Useremail=email, id=request.session.get("userid")).count()
        x = emailnews.objects.filter(userid=request.session.get("userid")).count()
        print(x)
        print(count)
        if count > 0:
            if x > 0:
                print("update")
                if not emailnews.objects.values_list('subscription', flat=True).get(
                        userid=request.session.get("userid")):
                    messages.info(request, "Email subscription has been updated, you will receive new mails !")
                emailnews.objects.filter(userid=request.session.get("userid")).update(subscription=True)
                message_name = "Aim Arena"
                message = "Thank you for subscribing to our newsletter ! You will receive latest updates and news of our services."
                message_email = email
                msg = EmailMessage(message_name,
                                   message,
                                   to=[message_email])
                msg.content_subtype = 'html'

                msg.send()
            else:
                new = emailnews()
                new.email = email
                new.userid = Userreg(request.session.get("userid"))
                new.subscription = True
                new.save()
                messages.info(request, "Your email is listed now, you will be notified with new news !")
        else:
            messages.error(request, "Please enter your email to be listed !")
        return redirect('game')
    else:
        return redirect('game')


def unsubscribe(request):
    x = emailnews.objects.values_list('subscription', flat=True).get(
        userid=request.session.get("userid"))
    if x:
        return render(request, "unsubscribe.html", {"x": x})
    else:
        return redirect('game')


def unsubscribebtn(request):
    if request.method == "POST":
        userid = request.session.get("userid")
        selectedvalue = request.POST.get("unsubscribe")
        message = None
        if selectedvalue == "other":
            message = request.POST.get("messagearea")

        if emailnews.objects.values_list('subscription', flat=True).get(
                userid=request.session.get("userid")):
            emailnews.objects.filter(userid=request.session.get("userid")).update(subscription=False)
            emailnewsid = emailnews.objects.get(userid=request.session.get("userid")).pk
            feedback = unsubscribefeedback()
            feedback.emailnewid = emailnews(emailnewsid)
            feedback.message = message
            feedback.feedbackname = selectedvalue
            feedback.save()
            messages.info(request, "You have been unsubscribed! thanks for your feedback")
            return redirect('unsubscribe')
        else:
            return redirect('game')
    else:
        return redirect('unsubscribe')