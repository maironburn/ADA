from django.db import models
from datetime import datetime
from ruleset.models import Ruleset
from api_authentication.models import User
import django.db.models.options as options
import json


# Create your models here.

class Tokencontrol(models.Model):

    token = models.TextField(blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 

