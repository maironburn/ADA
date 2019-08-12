from django.db import models
from datetime import datetime
import django.db.models.options as options
from django.contrib.auth.models import Group
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Elkquery(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    sql = models.TextField(blank=True, null=True)
    sql_ddl = models.TextField(blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

