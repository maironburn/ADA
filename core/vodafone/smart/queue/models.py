from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class TableQueue(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    title = models.CharField(max_length=24, blank=True, null=True)
    s_title = models.CharField(max_length=24, blank=True, null=True)
    shared_pers = models.FloatField(blank=True, null=True)
    allow_case = models.FloatField(blank=True, null=True)
    allow_subcase = models.FloatField(blank=True, null=True)
    allow_probdesc = models.FloatField(blank=True, null=True)
    allow_dmnd_dtl = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    sort_by = models.CharField(max_length=80, blank=True, null=True)
    max_resp_time = models.FloatField(blank=True, null=True)
    obj_received = models.FloatField(blank=True, null=True)
    obj_accepted = models.FloatField(blank=True, null=True)
    obj_forwarded = models.FloatField(blank=True, null=True)
    obj_rejected = models.FloatField(blank=True, null=True)
    obj_dispatched = models.FloatField(blank=True, null=True)
    obj_escalated = models.FloatField(blank=True, null=True)
    legal_obj_type = models.FloatField(blank=True, null=True)
    icon_id = models.FloatField(blank=True, null=True)
    allow_bug = models.FloatField(blank=True, null=True)
    dialog_id = models.FloatField(blank=True, null=True)
    department = models.CharField(max_length=80, blank=True, null=True)
    allow_opp = models.FloatField(blank=True, null=True)
    allow_contract = models.FloatField(blank=True, null=True)
    allow_job = models.FloatField(blank=True, null=True)
    allow_task = models.FloatField(blank=True, null=True)
    dev = models.FloatField(blank=True, null=True)
    queue2monitor = models.FloatField(blank=True, null=True)
    queue2dist_srvr = models.FloatField(blank=True, null=True)
    x_visibilidad = models.CharField(max_length=15, blank=True, null=True)
    allow_dialogue = models.FloatField(blank=True, null=True)
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    x_wmt = models.CharField(max_length=1, blank=True, null=True)
    x_descripcion = models.CharField(max_length=80, blank=True, null=True)
    x_fecha_creacion = models.DateTimeField(blank=True, null=True)
    x_mail = models.CharField(max_length=80, blank=True, null=True)

    def __json_encode__(self):
        output={}
        for field in self._meta.fields:
            output[field.name]=getattr(self, field.name)
        return output  

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_QUEUE\"'
