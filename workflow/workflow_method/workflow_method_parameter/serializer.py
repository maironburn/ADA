from rest_framework import serializers
from .models import Workflow_method_parameter

class WorkflowmethodparameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow_method_parameter
        fields = '__all__'