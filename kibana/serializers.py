from rest_framework import serializers
from .models import Kibana

class KibanaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kibana
        fields = '__all__'

