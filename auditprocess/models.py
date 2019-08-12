from django.db import models
from datetime import datetime
from datetime import datetime, timedelta
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Auditprocess(models.Model):

    PROCESS_INCREMENTAL="Incremental"
    PROCESS_ONLY_BACKLOG="Only Backlog"
    PROCESS_ANALYSIS_BACKLOG="Analysis Backlog"

    process = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateTimeField(auto_now_add=False, null=True, editable=False)
    end_date = models.DateTimeField(auto_now_add=False, null=True, editable=False)
    timestamp_date = models.DateTimeField(auto_now_add=True, editable=False)
    initial_records = models.IntegerField(blank=True, null=True)
    final_records = models.IntegerField(blank=True, null=True)
    pid = models.CharField(max_length=10, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)

    def setInitial(self, data):

        self.process=data["process"]        
        self.status="Initial"
        if ("pid" in data):
            self.pid=data["pid"]
        self.timestamp_date=datetime.now()
        self.start_date=datetime.now()
        if ("msg" in data):
            self.msg=data["msg"]
        self.save()

    def setInProgress(self, data):

        self.status="In progress"
        self.timestamp_date=datetime.now()
        if "initial_records" in data:
            self.initial_records=data["initial_records"]
        if ("msg" in data):
            self.msg=data["msg"]
        self.save()
    
    def setFinished(self, data):

        self.status="Finished"
        self.timestamp_date=datetime.now()
        if "final_records" in data:
            self.final_records=data["final_records"]
        self.end_date=datetime.now()
        if ("msg" in data):
            self.msg=data["msg"]
        self.save()
    
    def setCancelled(self, data):

        self.status="Cancelled"
        self.timestamp_date=datetime.now()
        if "final_records" in data:
            self.final_records=data["final_records"]
        self.end_date=datetime.now()
        if ("msg" in data):
            self.msg=data["msg"]
        self.save()

    def setError(self, data):

        self.status="Error"
        self.timestamp_date=datetime.now()
        self.end_date=datetime.now()
        if ("msg" in data):
            self.msg=data["msg"]
        self.save()

    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

