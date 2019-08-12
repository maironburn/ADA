from rest_framework import serializers
from core.vodafone.smart.x_clas_orden.models import XClasOrden

class SiteSerializer(serializers.ModelSerializer):

    class Meta:

        model = XClasOrden
        fields = '__all__'
