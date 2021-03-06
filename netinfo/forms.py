from django import forms
from netinfo.models import sites
from django.forms import ModelChoiceField

class SitesModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.name

class SitesForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'id', 'name':'id'})
    )
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'name', 'name':'name'})
    )
    alias_name = forms.CharField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'alias_name', 'name':'alias_name'})
    )
    SITE_TYPE = (('PP', 'PP'),('KK', 'KK'),('KCP', 'KCP'),('KC', 'KC'),('KP', 'KP'),('DC', 'DC'),('ISP', 'ISP'),('PARTNER', 'PARTNER'))
    type = forms.ChoiceField(
        label="Type",
        choices=SITE_TYPE,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'type', 'name':'type'})
    )
    location = forms.CharField(
        label="Location",
        max_length=300,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'location', 'name':'location', 'rows':3})
    )
    SITE_CITY = (('All City', 'All City'),('Yogyakarta', 'Yogyakarta'),('Gunungkidul', 'Gunungkidul'),('Kulon Progo', 'Kulon Progo'),('Bantul', 'Bantul'),('Sleman', 'Sleman'))
    city = forms.ChoiceField(
        label="City",
        choices=SITE_CITY,
        widget=forms.Select(attrs={'class': 'form-control', 'id' : 'city', 'name':'city'})
    )
    description = forms.CharField(
        label="Description",
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'description', 'name':'description', 'rows':2})
    )
    ip_address = forms.CharField(
        label="IP Address",
        max_length=100,
        required=False,
        initial='0.0.0.0/0',
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd', 'name':'ipadd' })
    )
    add_field1 = forms.CharField(
        label="Site code",
        max_length=3,
        required=False,
        help_text='Input 3 digits site code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'site_code', 'name':'site_code' })
    )
    add_field2 = forms.CharField(
        label="Area code",
        max_length=3,
        required=False,
        help_text='Input 3 digits area code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'area_code', 'name':'area_code', })
    )
    tagline = forms.CharField(
        label="Tagline",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2})
    )

class ContactsForm(forms.Form):
    id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={'class': 'form-control', 'name':'id'})
    )
    contact_type = forms.CharField(
        label="Type",
        widget=forms.TextInput(attrs={'class': 'form-control', 'name':'contact_type'})
    )
    contact_data = forms.CharField(
        label="Number",
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name':'contact_number', 'pattern': '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'})
    )
