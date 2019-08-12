from django.db import models
import django.db.models.options as options
from django.contrib.auth.models import Group

# Create your models here.

class Workflow(models.Model):

    groups = models.ManyToManyField(Group, blank=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    hide = models.TextField(blank=True, null=True)
    workflow_type = models.CharField(max_length=40, blank=True, null=True)

    def isAuthorized(self, user):
       belong=False
       for group in self.groups.all():
         if group in user.groups.all():
               belong=True
               break
       return belong      
       

    class Meta:
        ordering = ('id',)