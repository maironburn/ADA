from django.db import models
from core.validators import ApiADAValidator
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Classification(models.Model):

    name = models.TextField(blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    cod_apertura = models.TextField(blank=False, null=False)
    subcodigo = models.TextField(blank=False, null=False)
    plantilla = models.TextField(blank=False, null=False,  validators=[ApiADAValidator.validateJSONField])

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

