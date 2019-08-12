from rest_framework import serializers
from .models import Analysiserror

class AnalysiserrorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analysiserror
        fields = '__all__'


