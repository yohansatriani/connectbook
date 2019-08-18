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
        help_text='Example : 192.168.1.1 or 192.168.1.0/24',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'ipadd', 'name':'ipadd', 'pattern': '^(([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5]).){3}([0-9]|[1-9][0-9]|1[0-9]{2}|[1-2][0-4][0-9]|25[0-5])((/[0-9]|/[1-2][0-9]|/[1-3][0-2])?)$'})
    )
    add_field1 = forms.CharField(
        label="Site code",
        max_length=3,
        required=False,
        help_text='Input 3 digits site code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'site_code', 'name':'site_code', 'pattern': '\d{3}'})
    )
    add_field2 = forms.CharField(
        label="Area code",
        max_length=3,
        required=False,
        help_text='Input 3 digits area code',
        widget=forms.TextInput(attrs={'class': 'form-control', 'id' : 'area_code', 'name':'area_code', 'pattern': '\d{3}'})
    )
    tagline = forms.CharField(
        label="Tagline",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id' : 'tagline', 'name':'tagline', 'rows':2})
    )