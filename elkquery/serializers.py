from rest_framework import serializers
from .models import Elkquery

class ElkquerySerializer(serializers.ModelSerializer):       
    
    class Meta:
        model = Elkquery
        fields = '__all__'


