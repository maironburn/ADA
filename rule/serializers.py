from rest_framework import serializers
from condition.serializers import ConditionSerializer
from action.serializers import ActionSerializer
from .models import Rule

class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = '__all__'

class RuleSerializerDeep(serializers.ModelSerializer):

    condition=ConditionSerializer(required=True)
    actions=ActionSerializer(required=True, many=True)
    
    class Meta:
        model = Rule
        fields = ('id', 'description', 'ruleset', 'order', 'condition', 'actions', 'status')
		