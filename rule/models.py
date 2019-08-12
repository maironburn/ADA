from django.db import models
from datetime import datetime
from ruleset.models import Ruleset
from condition.models import Condition
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Rule(models.Model):

    description = models.TextField(blank=True, null=True)
    ruleset = models.ForeignKey(Ruleset, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=False)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('order',)
        fields_searchable = '__all__'
