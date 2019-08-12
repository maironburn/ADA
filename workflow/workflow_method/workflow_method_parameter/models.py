from django.db import models
import django.db.models.options as options
from workflow.workflow_method.models import Workflow_method
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Workflow_method_parameter(models.Model):

    workflow_method = models.ForeignKey(Workflow_method, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    optional = models.NullBooleanField(blank=True, null=True, default=False)

    def isAuthorized(self, user):
       return self.workflow_method.isAuthorized(user)

    class Meta:
        ordering = ('id',)
        fields_searchable = ('workflow_method',)