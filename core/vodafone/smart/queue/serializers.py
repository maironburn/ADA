from rest_framework import serializers
from .models import TableQueue

class TableQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableQueue
        fields = ('s_title',)