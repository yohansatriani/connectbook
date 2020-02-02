import json
from pprint import pprint

from django.template.loader import get_template, render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.serializers.json import DjangoJSONEncoder

from netinfo.models import sites as sites_model, contacts as contacts_model
from cms.models import contact_types as contact_types_model

from netinfo.forms import SitesForm, ContactsForm

# Create your views here.
@login_required()
def sites(request):
    #get all site data
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
    #if request method is POST
    if request.method == 'POST':
        #catch post data to variable
        site_post_data = {
            'id':1000,
            'name':request.POST['name'],
            'alias_name': "site",
            'description':request.POST['description'],
            'type':request.POST['type'],
            'location':request.POST['location'],
            'city':request.POST['city'],
            'add_field1':request.POST['add_field1'],
            'add_field2':request.POST['add_field2'],
            'ip_address':request.POST['ip_address'],
            'tagline':request.POST['tagline']
        }
        #insert post data to form
        site_form = SitesForm(site_post_data)
        #check unique site name
        validsite = sites_model.objects.filter(name=site_post_data['name'].strip()).count()+sites_model.objects.filter(alias_name=site_post_data['name'].strip()).count()
        #if site name unique do this
        if validsite == 0:
            #if site form valid
            if site_form.is_valid():
                #clean site post data
                name = site_form.cleaned_data['name']
                alias_name = name.replace(' ', '-').lower()
                type = site_form.cleaned_data['type']
                location = site_form.cleaned_data['location']
                city = site_form.cleaned_data['city']
                description = site_form.cleaned_data['description']
                ip_address = site_form.cleaned_data['ip_address']
                add_field1 = site_form.cleaned_data['add_field1']
                add_field2 = site_form.cleaned_data['add_field2']
                tagline = site_form.cleaned_data['tagline']
                #add site to database
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
                #commit add site
                sites_add.save()
                #if contact post data not empty
                if 'contact_data[]' in request.POST:
                    #catch contact post data
                    contacts_post_add_dataraw = [
                        request.POST.getlist('contact_type[]'),
                        request.POST.getlist('contact_data[]'),
                    ]
                    #transpose contact post data
                    contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))
                    #insert contact to database
                    for contacts_post_add in contacts_post_add_data:
                        contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_data=contacts_post_add[1]).save()

                #generate message
                messages.success(request, "Site "+sites_add.name+" added succesfully. For more information <a href=../name/"+sites_add.name+">Click Here</a>", extra_tags="success")
                return redirect('sites_add')
            #if site form invalid
            else:
                #generate message
                messages.error(request, 'Failed add Site.', extra_tags='danger')
                return redirect('sites_add')
        #if site name already exist
        else:
            #generate message
            messages.error(request, "Unable to add site. A site with name "+site_post_data['name']+" already exist.", extra_tags='error')
            return redirect('sites_add')
    #if request method is GET
    else:
        #get contact type
        contact_types = contact_types_model.objects.values('contact_type')
        #generate site form
        site_form = SitesForm()
        #breadcrumbs
        bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
        return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form, 'contact_types': contact_types})

@login_required()
def sites_edit(request, alias_name):
    #get site data by aliasname
    site_data = get_object_or_404(sites_model, alias_name=alias_name)
    return redirect('sites_edit_id', site_data.id)

@login_required()
def sites_edit_id(request, site_id):
    #if request method is POST
    if request.method == 'POST':
        #catch post data
        site_post_data = {
            'id':int(request.POST['id']),
            'name':request.POST['name'].strip(),
            'alias_name': request.POST['name'].strip().replace(' ', '-').lower(),
            'description':request.POST['description'],
            'type':request.POST['type'],
            'location':request.POST['location'],
            'city':request.POST['city'],
            'add_field1':request.POST['add_field1'],
            'add_field2':request.POST['add_field2'],
            'ip_address':request.POST['ip_address'],
            'tagline':request.POST['tagline']
        }
        #get site data from database
        site_data = sites_model.objects.get(id=int(request.POST['id']))
        #insert site data to list
        site_db_data = {
            'id': site_data.id,
            'name': site_data.name,
            'alias_name': site_data.alias_name,
            'description':site_data.description,
            'type': site_data.type,
            'location': site_data.location,
            'city': site_data.city,
            'add_field1': site_data.add_field1,
            'add_field2': site_data.add_field2,
            'ip_address': site_data.ip_address,
            'tagline': site_data.tagline,
        }
        #contact update process
        site_id = int(request.POST['id'])
        #contact update/edit
        if 'contact_id[]' in request.POST:
            contacts_post_data_raw = [
                request.POST.getlist('contact_id[]'),
                request.POST.getlist('contact_type[]'),
                request.POST.getlist('contact_data[]'),
            ]
            # transpose post data
            contacts_post_data_zip=list(map(list, zip(*contacts_post_data_raw)))
            #contact update process
            for contacts_post_data_list in contacts_post_data_zip:
                contacts_data = contacts_model.objects.get(id=int(contacts_post_data_list[0]))
                contacts_db_data = {
                    'id': contacts_data.id,
                    'contact_type': contacts_data.type,
                    'contact_data':contacts_data.contact_data,
                }
                contacts_post_data = {
                    'id': contacts_post_data_list[0],
                    'contact_type': contacts_post_data_list[1],
                    'contact_data': contacts_post_data_list[2],
                }
                contact_form = ContactsForm(contacts_post_data, initial=contacts_db_data)
                if contact_form.is_valid():
                    if contact_form.has_changed():
                        for changed_data in contact_form.changed_data:
                            setattr(contacts_data, changed_data, contacts_post_data[changed_data])
                            contacts_data.save()

        #contact add
        if 'contact_data[]' in request.POST:
            #catch contact post data
            contacts_post_add_dataraw = [
                request.POST.getlist('contact_type_add[]'),
                request.POST.getlist('contact_data_add[]'),
            ]
            #transpose contact post data
            contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))
            #insert contact to database
            for contacts_post_add in contacts_post_add_data:
                contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_data=contacts_post_add[1]).save()
        #contact delete
        if 'contact_id_del[]' in request.POST:
            #store deleted contact id
            post_contacts_id_del = request.POST.getlist('contact_id_del[]')
            #contact delete process
            for contact_id in post_contacts_id_del:
                contacts_data = contacts_model.objects.get(id=contact_id)
                contacts_data.delete()
        #site update process
        #insert post data for site form
        site_form = SitesForm(site_post_data)
        #check unique site name
        validsite = sites_model.objects.filter(name=site_post_data['name'].strip()).count()+sites_model.objects.filter(alias_name=site_post_data['name'].strip()).count()
        #if site name unique do this or site name not changed
        if (validsite == 0) or (site_post_data['name'] == site_db_data['name']):
            #declare site form  with initial site db data
            site_form = SitesForm(site_post_data, initial=site_db_data)
            #check if site form is valid
            if site_form.is_valid():
                #check changed data on form
                if site_form.has_changed():
                    #update data on site data if data changed
                    for changed_data in site_form.changed_data:
                        setattr(site_data, changed_data, site_post_data[changed_data])
                        site_data.save()
                    #generate message
                    messages.success(request, "Site "+site_post_data['name']+" edited succesfully.", extra_tags="success")
                    return redirect('sites_detail_id', site_id)
                #if no changed data
                else:
                    #generate message
                    messages.info(request, "No changed data on Site "+site_post_data['name']+".", extra_tags="info")
                    return redirect('sites_detail_id', site_id)
            #if site form is invalid
            else:
                #generate message
                messages.error(request, 'Failed updating Site Information.', extra_tags='alert-danger')
                return redirect('sites_edit_id', site_id)
        else:
            #generate message
            messages.error(request, "Unable to edit site. Site "+site_post_data['name']+" already exist.", extra_tags='error')
            return redirect('sites_edit_id', site_id)

    #    if validsite == 0:
    #        if site_form.is_valid():
    #            type = site_form.cleaned_data['type']
    #            location = site_form.cleaned_data['location']
    #            city = site_form.cleaned_data['city']
    #            description = site_form.cleaned_data['description']
    #            add_field1 = site_form.cleaned_data['add_field1']
    #            add_field2 = site_form.cleaned_data['add_field2']
    #            tagline = site_form.cleaned_data['tagline']
    #            alias_name = name.replace(' ', '-').lower()
    #
    #            sites_add = sites_model(
    #                name=name,
    #                alias_name = alias_name,
    #                type=type,
    #                location=location,
    #                city=city,
    #                description=description,
    #                ip_address=ip_address,
    #                add_field1=add_field1,
    #                add_field2=add_field2,
    #                tagline=tagline,
    #            )
    #             sites_add.save()
    #             site_id = sites_add.id;
    #             messages.success(request, "Site "+sites_add.name+" added succesfully. For more information <a href=../name/"+sites_add.name+">Click Here</a>", extra_tags="success")
    #
    #             pprint(messages)
    #
    #             if 'contact_data[]' in request.POST:
    #                 contacts_post_add_dataraw = [
    #                     request.POST.getlist('contact_type[]'),
    #                     request.POST.getlist('contact_data[]'),
    #                 ]
    #                 contacts_post_add_data=list(map(list, zip(*contacts_post_add_dataraw)))
    #
    #                 for contacts_post_add in contacts_post_add_data:
    #                     contacts_model(site=sites_model.objects.get(id=int(site_id)), type=contacts_post_add[0], contact_data=contacts_post_add[1]).save()
    #                     # messages.success(request, "Contact: "+contacts_post_add[0]+":"+contacts_post_add[1]+" added succesfully." , extra_tags='alert-success')
    #
    #             return redirect('sites_add')
    #
    #         else:
    #             messages.error(request, 'Failed add Site.', extra_tags='danger')
    #             bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/add/', 'Add Site']]
    #             return render(request, 'netinfo/page_sites_add.html', {'title': "Add Site", 'head': "Add Site", 'bcitems': bcitems, 'site_form': site_form})
    #     else:
    #         messages.error(request, "Unable to add site. A site with name "+site_post_data['name']+" already exist.", extra_tags='error')
    #         return redirect('sites_add')
    #if request method is GET
    else:
        #check valid url
        try:
            site_id = int(site_id)
        except ValueError:
            raise Http404()
        #query site data from database
        site_data = get_object_or_404(sites_model, id=site_id)
        #delcare site form with
        site_form = SitesForm(initial={
            'id': site_id,
            'name': site_data.name,
            'alias_name': site_data.alias_name,
            'type': site_data.type,
            'location': site_data.location,
            'city': site_data.city,
            'description':site_data.description,
            'ip_address': site_data.ip_address,
            'add_field1': site_data.add_field1,
            'add_field2': site_data.add_field2,
            'tagline': site_data.tagline,
        })
        #get contact data & types
        contact_data = contacts_model.objects.filter(site_id = site_id)
        contact_types = contact_types_model.objects.values('contact_type')
        #breadcrumbs
        bcitems = [['/home/', 'Home'], ['#', 'Network Info'], ['/sites/', 'Sites'],['/sites/name/'+site_data.alias_name+'/', site_data.name], ['Edit', 'Edit']]
        return render(request, 'netinfo/page_sites_edit.html', {'title': "Edit Site", 'head': "Edit Site", 'bcitems': bcitems, 'site_form': site_form, 'contact_data': contact_data, 'contact_types': contact_types, 'site_id':site_id})

@login_required()
def sites_delete(request):
    #if request method POST
    if request.method == 'POST':
        #catch site id
        site_id = request.POST['site_id']
        #query site data from database
        site_del = get_object_or_404(sites_model, id=site_id)
        #store site name
        site_name = site_del.name
        #delete site
        site_del.delete()
        #generate message
        messages.success(request, "Site "+site_name+" deleted succesfully.", extra_tags='success')
        return redirect('sites')
    #if request method GET
    else:
        return redirect('sites')
