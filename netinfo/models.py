from django.db import models

# Create your models here.
class sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=300, default='')
    city = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    ipadd = models.CharField(max_length=100, default='0.0.0.0/0')
    tagline = models.CharField(max_length=500, default='')

    class Meta:
        verbose_name_plural = "sites"

    def __str__(self):
        return u'%s %s %s %s %s %s %s %s %s %s' %(
            self.id, self.name, self.type, self.location, self.city, self.description, self.ipadd, self.site_code, self.area_code, self.tagline
        )
