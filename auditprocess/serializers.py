from rest_framework import serializers
from .models import Auditprocess
import datetime

class AuditprocessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auditprocess
        fields = '__all__'

