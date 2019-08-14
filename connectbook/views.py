from django.template import Template, Context
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def inspinia(request):
    return render(request, '.inspinia/page_home_ori.html', {'title': "INSPINIA", 'head': "INSPINIA"})

def error404(request, exception):
    return render(request, 'error/404.html', status = 404)

def error500(request):
    return render(request, 'error/500.html', status = 500)

#def sites_detail(request):
#    return render(request, 'netinfo/page_sites_detail.html', {'title': "Sites Detail", 'head': "Sites Detail"})

def auth_login(request):
    if not request.user.is_authenticated:
        return render(request, 'accounts/login.html', {'title': "Login", 'head': "Login"})
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
    bcitems = [['/home/', 'Home']]
    return render(request, 'home/page_home.html', {'title': "Home", 'head': "Home"})
