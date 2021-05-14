from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def home(request):
    userid = request.session.get('userid')
    if not userid:
        return redirect('signin')
    return render(request, 'home.html')


def error_404_view(request, exception):
    return render(request, 'Error404.html')
