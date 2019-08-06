from django.template.loader import get_template, render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from netinfo.models import sites as sites_model

# Create your views here.
@login_required()
def sites(request):
    sites_data = sites_model.objects.all()

    bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites']]
    return render(request, 'netinfo/page_sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'sites_data': sites_data})
