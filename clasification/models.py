from django.db import models
from core.validators import ApiADAValidator
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Clasification(models.Model):
    
    TYPE_CONTRACT_IN_PROGRESS = 'CRM Contract in progress'
    TYPE_INTERNAL_ERROR = 'CRM Internal Error'
    TYPE_CONTRACT_NOT_DEFINED = 'CRM Contract not defined'
    TYPE_CONTRACT_WRONG_NAMED = 'CRM Contract wrong named'

    type = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    metadata = models.TextField(blank=False, null=False,  validators=[ApiADAValidator.validateJSONField])
    editable = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

