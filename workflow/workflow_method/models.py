from django.db import models
import django.db.models.options as options
from workflow.models import Workflow
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Workflow_method(models.Model):

    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    class_method = models.TextField(blank=True, null=True)
    serializer_method = models.TextField(blank=True, null=True)
    output_description = models.TextField(blank=True, null=True)

    def isAuthorized(self, user):
       return self.workflow.isAuthorized(user)

    class Meta:
        ordering = ('id',)
        fields_searchable = ('workflow','name')
        permissions = (("execute_workflow_method", "Can execute workflow_method"),)