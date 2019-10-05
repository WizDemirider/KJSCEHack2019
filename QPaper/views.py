from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import escape

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("Welcome!")

def signupUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password1'])
        raw_password2 = escape(request.POST['password2'])
        try:
            if raw_password == raw_password2 and len(raw_password) >= 6:
                user = User.objects.create(username=username, password=raw_password)
                user.set_password(raw_password)
                user.save()
                login(request, user) # logs User in
                return redirect('home')
            elif len(raw_password) >= 6:
                return render(request, 'Authentication/signup.html', {'error': "Passwords do not match!"})
            else:
                return render(request, 'Authentication/signup.html', {'error': "Password must be 6 characters or more"})
        except Exception as e:
            return render(request, 'Authentication/signup.html', {'error': str(e)})
    return render(request, 'Authentication/signup.html', {'error': None})

def loginUser(request):
    if request.method == 'POST':
        username = escape(request.POST['username'])
        raw_password = escape(request.POST['password'])
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(request, user) # logs User in
            return redirect('home')
        else:
            return render(request, 'Authentication/signup.html', {'error': "Unable to Log you in!"})
    return render(request, 'Authentication/login.html', {'error': None})

def logoutUser(request):
    logout(request)
    return redirect('index')

@login_required
def home(request):
    return HttpResponse("your dashboard")
