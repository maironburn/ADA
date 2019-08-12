from rest_framework import serializers
from .models import Rulefunction

class RulefunctionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rulefunction
        fields = '__all__'


