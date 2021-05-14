from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import game, terms, privacy, leaderboards, contact, contactus, emaillist, unsubscribe, unsubscribebtn, about

urlpatterns = [
    path('', game, name="game"),
    path('/emailnews/', emaillist, name="emailnews"),
    path('/unsubscribe/', unsubscribe, name="unsubscribe"),
    path('/unsubscribe/unsubscribebtn', unsubscribebtn, name="unsubscribebtn"),
    path('/terms/', terms, name="terms"),
    path('/privacy/', privacy, name="privacy"),
    path('/leaderboards/', leaderboards, name="leaderboards"),
    path('/contact-us/', contact, name="contact"),
    path('/about-us/', about, name="about"),
    path('/contact-us/sendmessage/', contactus, name="contactsendmsg"),
]