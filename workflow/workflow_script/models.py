from django.db import models
import django.db.models.options as options
from workflow.models import Workflow
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Workflow_script(models.Model):

    workflow=models.ForeignKey(Workflow, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    def isAuthorized(self, user):
       return self.workflow.isAuthorized(user)

    class Meta:
        ordering = ('id',)
        fields_searchable = ('workflow',)