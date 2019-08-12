from rest_framework import serializers
from .models import Condition

class ConditionSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
            """
            Update and return an existing `condition` instance, given the validated data.
            """
            instance.logicalcondition = validated_data.get('logicalcondition', instance.logicalcondition)
            instance.save()
            return instance
    
    class Meta:
        model = Condition
        fields = '__all__'


