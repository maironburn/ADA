from rest_framework import serializers
from .models import Ruleoperator

class RuleoperatorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ruleoperator
        fields = '__all__'


