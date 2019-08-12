from django.db import models
import django.db.models.options as options
from core.vodafone.smart.privclass.models import Privclass
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class User(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    s_login_name = models.CharField(max_length=30, blank=True, null=True)
    user_access2privclass = models.ForeignKey(Privclass, on_delete=models.CASCADE, db_column='user_access2privclass')
    

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_USER\"'

