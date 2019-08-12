from rest_framework import serializers
from .models import Pattern

class PatternSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
            """
            Update and return an existing `pattern` instance, given the validated data.
            """
            instance.pattern = validated_data.get('pattern', instance.pattern)
            instance.label = validated_data.get('label', instance.label)
            instance.description = validated_data.get('description', instance.description)
            instance.priority = validated_data.get('priority', instance.priority)
            instance.enable = validated_data.get('enable', instance.enable)
            instance.save()
            return instance

    class Meta:
        model = Pattern
        fields = '__all__'


