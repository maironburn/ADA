from django.db import models
from ApiADA.constantes import Constantes
from django.core.validators import RegexValidator
from appparameter.models import Appparameter
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Pattern(models.Model):

    try:
        pattern = models.TextField(blank=True, null=False, validators=[RegexValidator(Appparameter.objects.get(name='Field pattern validator').getParamaterDataValue(), message='Invalid value, only the following characters are allowed (a-z, A-Z, 0-9, . , *, ,-,_)')])
    except:
        pattern = models.TextField(blank=True, null=False, validators=[RegexValidator('[a-zA-Z0-9.*\\-_ #]+$', message='Invalid value, only the following characters are allowed (a-z, A-Z, 0-9, . , *, ,-,_)')])
    label = models.CharField(max_length=255, blank=True, null=False)
    description = models.CharField(max_length=255, blank=True, null=False)
    priority = models.FloatField(blank=True, null=False)
    enable = models.BooleanField(default=False, null=False)

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
