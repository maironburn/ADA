from django.db import models
from datetime import datetime
from rule.models import Rule
from .validators import ActionValidator
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Action(models.Model):

    logicalaction = models.TextField(blank=True, null=True, validators=[ActionValidator.validateAction])
    order = models.IntegerField(blank=True, null=False)
    rule = models.ForeignKey(Rule, related_name='actions', on_delete=models.CASCADE)

    class Meta:
        ordering = ('order',)
        fields_searchable = '__all__'
