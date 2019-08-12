from rest_framework import serializers
from .models import Workflow_script

class WorkflowScriptSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow_script
        fields = '__all__'