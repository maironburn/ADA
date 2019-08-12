from django.db import models
from datetime import datetime
import django.db.models.options as options
import json
from .validators import ConditionValidator
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Condition(models.Model):

    logicalcondition = models.TextField(blank=True, null=True, validators=[ConditionValidator.validateCondition])

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
