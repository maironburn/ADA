from rest_framework import serializers
from core.vodafone.smart.site.models import Site

class SiteSerializer(serializers.ModelSerializer):

    class Meta:

        model = Site
        fields = ('objid', 'site_id', 'update_stamp', 'x_estado_catv', 'x_estado_cliente', 'x_estado_dtv', 'x_estado_int', 'x_estado_tlf', 'x_tipo_clte', 'x_tipo_ggcc', 'x_estado_int_ull', 'x_estado_tlf_ull', 'x_estado_mv', 'x_estado_adsli', 'x_estado_ai', 'x_jerarquia', 'x_child_site2x_site', 'x_tecnologia_ins', 'x_fecha_migracion', 'x_tecnologia_ins_mig')
