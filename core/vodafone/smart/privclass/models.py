from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class Privclass(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    s_class_name = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_PRIVCLASS\"'

