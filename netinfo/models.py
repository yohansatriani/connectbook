from django.db import models

# Create your models here.
class sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=300, default='', null=True)
    city = models.CharField(max_length=100, default='', null=True)
    description = models.CharField(max_length=1000, default='', null=True)
    ipadd = models.CharField(max_length=100, default='0.0.0.0/0', null=True)
    tagline = models.CharField(max_length=500, default='', null=True)

    class Meta:
        verbose_name_plural = "sites"

    def __str__(self):
        return u'%s %s %s %s %s %s %s %s' %(
            self.id, self.name, self.type, self.location, self.city, self.description, self.ipadd, self.tagline
        )

class contacts(models.Model):
    id = models.AutoField(primary_key=True)
    site = models.ForeignKey(sites, on_delete=models.CASCADE, null=False)
    type = models.CharField(max_length=10, null=False, default='')
    contact_number = models.CharField(max_length=50, null=False, default='')

    class Meta:
        verbose_name_plural = "contacts"

    def __str__(self):
        return u'%s %s' %(
            self.site, self.type
        )
