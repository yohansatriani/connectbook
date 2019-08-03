from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
#from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.decorators import login_required
#from django.db.models import Q
#from django.contrib import messages

from netinfo.models import sites as sites_model

# Create your views here.
@login_required()
def sites(request):
    site_data = sites_model.objects.all()

    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites']]
    return render(request, 'netinfo/page_sites.html', {'title': "CB | Login", 'head': "Login"})
    #return render(request, "netinf/page-sites.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data})
