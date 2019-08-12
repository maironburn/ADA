from django.db import models
from datetime import datetime
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Analysiserror(models.Model):

    averia = models.TextField(blank=True, null=True)
    event = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
