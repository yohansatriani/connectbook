from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def sites(request):
    site_data = sites_model.objects.all()

    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites']]
    return render(request, "netinfo/page-sites.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data})
