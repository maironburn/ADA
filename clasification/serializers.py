from rest_framework import serializers
from .models import Clasification

class ClasificationSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
            """
            Update and return an existing `Clasification` instance, given the validated data.
            """
            instance.type = validated_data.get('type', instance.type)
            instance.description = validated_data.get('description', instance.description)
            instance.metadata = validated_data.get('metadata', instance.metadata)
            instance.editable = validated_data.get('editable', instance.editable)
            instance.save()

            return instance
    
    class Meta:
        model = Clasification
        fields = '__all__'


