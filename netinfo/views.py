import json
from pprint import pprint

from django.template.loader import get_template, render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.serializers.json import DjangoJSONEncoder

from netinfo.models import sites as sites_model, contacts as contacts_model
from cms.models import contact_types as contact_types_model

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
    contact_data = contacts_model.objects.filter(site_id = site_data.id)
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
    contact_data = contacts_model.objects.filter(site_id = site_id)
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
            'add_field1':request.POST['add_field1'],
            'add_field2':request.POST['add_field2'],
            'ip_address':request.POST['ip_address'],
            'tagline':request.POST['tagline']
        }

        site_form = SitesForm(site_post_data)

        validsite = sites_model.objects.filter(name=site_post_data['name'].strip()).count()+sites_model.objects.filter(alias_name=site_post_data['name'].strip()).count()

        pprint(validsite)

        if validsite == 0:
            if site_form.is_valid():
                name = site_form.cleaned_data['name']
                type = site_form.cleaned_data['type']
                location = site_form.cleaned_data['location']
                city = site_form.cleaned_data['city']
                description = site_form.cleaned_data['description']
                ip_address = site_form.cleaned_data['ip_address']
                add_field1 = site_form.cleaned_data['add_field1']
                add_field2 = site_form.cleaned_data['add_field2']
                tagline = site_form.cleaned_data['tagline']

                alias_name = name.replace(' ', '-').lower()

                sites_add = sites_model(
                    name=name,
                    alias_name = alias_name,
                    type=type,
                    location=location,
                    city=city,
                    description=description,
                    ip_address=ip_address,
                    add_field1=add_field1,
                    add_field2=add_field2,
                    tagline=tagline,
                )
                sites_add.save()
                site_id = sites_add.id;
                messages.success(request, "Site "+sites_add.name+" added succesfully. For more information <a href=../name/"+sites_add.name+">Click Here</a>", extra_tags="success")

                pprint(messages)

                if 'contact_data[]' in request.POST:
                    contacts_post_add_dataraw = [
                        request.POST.getlist('contact_type[]'),
                        request.POST.getlist('contact_data[]'),
                    ]
                    contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))

                    for contacts_post_add in contacts_post_add_data:
                        contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_data=contacts_post_add[1]).save()
                        # messages.success(request, "Contact: "+contacts_post_add[0]+":"+contacts_post_add[1]+" added succesfully." , extra_tags='alert-success')

                return redirect('sites_add')

            else:
                messages.error(request, 'Failed add Site.', extra_tags='danger')
                bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
                return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})
        else:
            messages.error(request, "Unable to add site. A site with name "+site_post_data['name']+" already exist.", extra_tags='error')
            return redirect('sites_add')
    else:
        contact_types = contact_types_model.objects.values('contact_type')
        # contact_types_json = json.dumps(list(contact_types), cls=DjangoJSONEncoder)

        sites_form = SitesForm()

        #breadcrumbs
        bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
        return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'sites_form': sites_form, 'contact_types': contact_types})

@login_required()
def sites_delete(request):
    if request.method == 'POST':
        site_id = request.POST['site_id']
        site_del = get_object_or_404(sites_model, id=site_id)
        site_name = site_del.name
        site_del.delete()
        messages.success(request, "Site "+site_name+" deleted succesfully.", extra_tags='success')
        return redirect('sites')
    else:
        return redirect('sites')
