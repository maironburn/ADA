from rest_framework import serializers
from .models import Appparameter
import datetime

class AppparameterSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""
 
    def update(self, instance, validated_data):
        """
        Update and return an existing `Appparameter` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.module = validated_data.get('module', instance.module)
        instance.description = validated_data.get('description', instance.description)
        instance.parameter_type = validated_data.get('parameter_type', instance.parameter_type)
        instance.data = validated_data.get('data', instance.data)
        instance.metadata = validated_data.get('metadata', instance.metadata)
        instance.modified_by = validated_data.get('modified_by', instance.metadata)
        instance.modified_date = datetime.datetime.now()
        instance.save()
        return instance


    class Meta:
        model = Appparameter
        fields = '__all__'

