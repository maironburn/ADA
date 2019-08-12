from rest_framework import serializers
from core.vodafone.smart.privclass.models import Privclass

class PrivclassSerializer(serializers.ModelSerializer):

    class Meta:

        model = Privclass
        fields =  ('s_class_name',)
