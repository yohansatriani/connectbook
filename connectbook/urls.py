"""connectbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#login
from django.contrib.auth import views as auth_views

from connectbook.views import base, home, auth_login, auth_process, auth_logout
from netinfo.views import sites


urlpatterns = [
    #DJANGO ADMIN
    path('admin/', admin.site.urls),
    #BASE
    path('base/', base, name='base'),
    #LOGIN
    path('accounts/login/', auth_login, name='login'),
    #AUTH
    path('accounts/auth/', auth_process, name='auth'),
    #LOGOUT
    path('accounts/logout/', auth_logout, name='logout'),
    #BASE
    path('home/', home, name='home'),
]
