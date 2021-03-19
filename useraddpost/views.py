from django.shortcuts import render
from .models import Userreg, UserPost
# Create your views here.
def Addpost(request):
    context = {"item": UserPost.objects.all()}
    if request.method == "POST":



