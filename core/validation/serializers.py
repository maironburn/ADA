from rest_framework import serializers
from .models import Validation

class ValidationSerializer(serializers.Serializer):

    
    def to_internal_value(self, data):
        output={
                "code":data.code, 
                "msg":data.msg,
                "msgDetail":data.msgDetail
        }
        
        return output  


    def to_representation(self, instance):
        response_dict = dict()
        response_dict = {
            'code' : instance.code,
            'msg': instance.msg,
            'msgDetail': instance.msgDetail
        }
        return response_dict

    
    class Meta:
        model = Validation
        fields = ('code','msg','msgDetail')
