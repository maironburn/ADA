from django.db import models
from datetime import datetime
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Ruleoperator(models.Model):

    operator = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    numfields = models.IntegerField(blank=True, null=False)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

