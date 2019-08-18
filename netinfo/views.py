from django.template.loader import get_template, render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from netinfo.models import sites as sites_model, contacts as contacts_model

from netinfo.forms import SitesForm

# Create your views here.
@login_required()
def sites(request):
    site_data = sites_model.objects.order_by('type', 'name')

    #breadcrumbs
    bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites']]
    return render(request, 'netinfo/page_sites.html', {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data})

@login_required()
def sites_detail(request, alias_name):
    try:
        alias_name = alias_name
    except ValueError:
        raise Http404()
    #site info
    site_data = get_object_or_404(sites_model, alias_name=alias_name)
    #contact info
    contact_data = contacts_model.objects.filter(site = site_data.id)
    #link info
    #links_data = links_model.objects.filter(Q(sites1=site_id)|Q(sites2=site_id))
    #device info
    #dev_data = dev_model.objects.filter(location_id = site_id)
    #breadcrumbs
    bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'], [alias_name, site_data.name]]
    return render(request, "netinfo/page_sites_detail.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data, 'contact_data': contact_data})

@login_required()
def sites_detail_id(request, site_id):
    try:
        site_id = int(site_id)
    except ValueError:
        raise Http404()
    #site info
    site_data = get_object_or_404(sites_model, id=site_id)
    #contact info
    contact_data = contacts_model.objects.filter(site = site_id)
    #link info
    #links_data = links_model.objects.filter(Q(sites1=site_id)|Q(sites2=site_id))
    #device info
    #dev_data = dev_model.objects.filter(location_id = site_id)
    #breadcrumbs
    bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'], [site_id, site_data.name]]
    return render(request, "netinfo/page_sites_detail.html", {'title': "Sites", 'head': "Sites", 'bcitems': bcitems, 'site_data': site_data, 'contact_data': contact_data})

@login_required()
def sites_add(request):
    if request.method == 'POST':
        site_post_data = {
            'id':1000,
            'name':request.POST['name'],
            'description':request.POST['description'],
            'type':request.POST['type'],
            'location':request.POST['location'],
            'city':request.POST['city'],
            'site_code':request.POST['site_code'],
            'area_code':request.POST['area_code'],
            'ip_address':request.POST['ip_address'],
            'tagline':request.POST['tagline']
        }

        site_form = SiteForm(site_post_data)

        if site_form.is_valid():
            name = site_form.cleaned_data['name']
            type = site_form.cleaned_data['type']
            location = site_form.cleaned_data['location']
            city = site_form.cleaned_data['city']
            description = site_form.cleaned_data['description']
            ip_address = site_form.cleaned_data['ip_address']
            site_code = site_form.cleaned_data['site_code']
            area_code = site_form.cleaned_data['area_code']
            tagline = site_form.cleaned_data['tagline']

            sites_add = sites_model(
                name=name,
                type=type,
                location=location,
                city=city,
                description=description,
                ip_address=ip_address,
                site_code=site_code,
                area_code=area_code,
                tagline=tagline,
            )
            sites_add.save()
            site_id = sites_add.id;
            messages.success(request, "Site added succesfully.", extra_tags='alert-success')

            if 'add_contact_id' in request.POST:
                contacts_post_add_dataraw = [
                    request.POST.getlist('add_contact_type'),
                    request.POST.getlist('add_contact_number'),
                ]
                contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))
                for contacts_post_add in contacts_post_add_data:
                    contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_number=contacts_post_add[1]).save()
                    messages.success(request, "Contact: "+contacts_post_add[0]+":"+contacts_post_add[1]+" added succesfully." , extra_tags='alert-success')

            return redirect('site_detail', site_id=site_id)

        else:
            messages.error(request, 'Failed add Site.', extra_tags='alert-danger')
            bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
            return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})
    else:
        sites_form = SitesForm()

        #breadcrumbs
        bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
        return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'sites_form': sites_form})
