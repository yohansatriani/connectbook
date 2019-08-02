from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def base(request):
    html = render_to_string('page_base.html')
    return HttpResponse(html)

def auth_login(request):
    if not request.user.is_authenticated:
        return render(request, 'account_login.html', {'title': "CB | Login", 'head': "Login"})
    else:
        return redirect(home)

def auth_process(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_url = request.POST['next']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect(home)
        else:
            messages.error(request,'Authentication Failed: Username or password is incorrect')
            return redirect(auth_login)
    else:
        if not request.user.is_authenticated:
            return redirect(auth_login)
        else:
            return redirect(home)

def auth_logout(request):
    logout(request)
    return redirect(auth_login)

@login_required()
def home(request):
    html = render_to_string('page_home_dashboard.html', {'title': "Home", 'head': "Home", 'bcitems': [['home', 'Home']]})
    return HttpResponse(html)
