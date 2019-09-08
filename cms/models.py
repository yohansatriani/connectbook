from django.db import models

# Create your models here.
class contact_types(models.Model):
    id = models.AutoField(primary_key=True)
    contact_type = models.CharField(max_length=100, unique=True, null=False)

    class Meta:
        verbose_name_plural = "contact_types"

    def __str__(self):
        return u'%s %s' %(
            self.id, self.contact_type
        )
