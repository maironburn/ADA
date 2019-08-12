from django.db import models
from datetime import datetime
import django.db.models.options as options
import json
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)

# Create your models here.

class Appparameter(models.Model):

    name = models.CharField(max_length=255, blank=True, null=True)
    module = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parameter_type = models.CharField(max_length=40, blank=True, null=True)
    data = models.TextField(blank=True, null=True)
    metadata = models.TextField(blank=True, null=True)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    hidden = models.BooleanField(default=False)

    def getParamaterDataValue(self):

        objData=json.loads(self.data)
        objMetada=json.loads(self.metadata)
        
        if self.parameter_type=='value':
            fieldName=objMetada['fields']
            return objData[fieldName]
        elif self.parameter_type=='list_of_values':
            fieldName=objMetada['fields']                        
            output=[]
            for item in objData[fieldName]:
                output.append(item)
            return output    
        elif self.parameter_type=='list_of_objects':
            return objData
        elif self.parameter_type=='datetime':
            fieldName=objMetada['fields']
            formatDate=objMetada['format']
            return datetime.strptime(objData[fieldName], formatDate)

    def setParameterDataValue(self, values):

        objMetada=json.loads(self.metadata)

        if self.parameter_type=='value':
            fieldName=objMetada['fields']
            objData={fieldName : values}
            self.data=json.dumps(objData)
        elif self.parameter_type=='list_of_values':
            fieldName=objMetada['fields']                        
            objData={fieldaName : values}
            self.data=json.dumps(objData)
        elif self.parameter_type=='list_of_objects':
            self.data=json.dumps(values)
        elif self.parameter_type=='datetime':
            fieldName=objMetada['fields']
            formatDate=objMetada['format']
            objData={fieldName : values.strftime(formatDate)}
            self.data=json.dumps(objData)


    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'

