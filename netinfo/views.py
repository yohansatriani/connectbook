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

@login_required()
def sites_detail(request, site_id):
    try:
        site_id = int(site_id)
    except ValueError:
        raise Http404()
    #site info
    site_data = get_object_or_404(sites_model, id=site_id)
    #contact info
    #contacts_data = contacts_model.objects.filter(site = site_id)
    #link info
    #links_data = links_model.objects.filter(Q(sites1=site_id)|Q(sites2=site_id))
    #device info
    #dev_data = dev_model.objects.filter(location_id = site_id)
    # breadcrumbs
    bcitems = [['/home/', 'Home'], ['/sites/', 'Sites'], [site_id, site_data.name]]
    return render(request, "netinfo/page-sites-detail.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data , 'contacts_data': contacts_data})
