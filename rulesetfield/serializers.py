from rest_framework import serializers
from .models import Rulesetfield

class RulesetfieldSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
            """
            Update and return an existing `rutesetfield` instance, given the validated data.
            """
            instance.field = validated_data.get('field', instance.field)
            instance.ruleset = validated_data.get('ruleset', instance.ruleset_id)
            instance.save()
            return instance
    
    class Meta:
        model = Rulesetfield
        fields = '__all__'


