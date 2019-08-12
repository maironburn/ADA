from django.db import models
from datetime import datetime
from ruleset.models import Ruleset
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Rulesetfield(models.Model):

    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    field = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
