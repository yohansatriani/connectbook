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

from connectbook.views import inspinia, home, auth_login, auth_process, auth_logout
from netinfo.views import sites, sites_detail, sites_detail_id, sites_add, sites_delete, sites_id_edit

handler404 = 'connectbook.views.error404'
handler500 = 'connectbook.views.error500'

urlpatterns = [
    #INSPINIA
    path('inspinia/', inspinia, name='inspinia'),
    #DJANGO ADMIN
    path('admin/', admin.site.urls),
    #LOGIN
    path('accounts/login/', auth_login, name='login'),
    #AUTH
    path('accounts/auth/', auth_process, name='auth'),
    #LOGOUT
    path('accounts/logout/', auth_logout, name='logout'),
    #BASE
    path('home/', home, name='home'),
    #SITES
    path('sites/', sites, name='sites'),
    #SITES_DETAIL
    path('sites/name/<slug:alias_name>/', sites_detail, name='sites_detail'),
    #SITES_DETAIL_ID
    path('sites/id/<int:site_id>/', sites_detail_id, name='sites_detail_id'),
    #SITES_ADD
    path('sites/add/', sites_add, name='sites_add'),
    #SITES_EDIT
    path('sites/id/<int:site_id>/edit/', sites_id_edit, name='sites_id_edit'),
    #SITES_DEL
    path('sites/del/', sites_delete, name='sites_delete'),
]
