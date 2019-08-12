from rest_framework import serializers
from .models import Ruleset

class RulesetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ruleset
        fields = '__all__'
