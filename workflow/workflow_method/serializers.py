from rest_framework import serializers
from .models import Workflow_method
from rest_framework.renderers import JSONRenderer
from ApiADA.constantes import Constantes


class WorkflowmethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow_method
        fields = '__all__'


                           


           