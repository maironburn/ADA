from rest_framework import serializers
from .models import Validationscript

class ValidationscriptSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
       response_dict = dict()
       response_dict = {
           'id' : instance.id,
           'name': instance.name,
           'description': instance.description,
           'belongto': instance.belongto,
           'order': instance.order,
           'status': instance.status,
           'classname': instance.classname,
           'code': instance.getCode()
       }
       return response_dict

    def update(self, instance, validated_data):
        """
        Update and return an existing `validationscript` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.belongto = validated_data.get('belongto', instance.belongto)
        instance.order = validated_data.get('order', instance.order)
        instance.status = validated_data.get('status', instance.status)
        instance.classname = validated_data.get('classname', instance.classname)
        instance.save()
        return instance

    class Meta:
        model = Validationscript
        fields = ('id','name','description','belongto','order','status','classname','code')
