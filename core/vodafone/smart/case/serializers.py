from rest_framework import serializers
from .models import TableCase

class TableCaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TableCase
        fields = ('title','id_number','creation_time','case_history','modify_stmp','case_type_lvl1','case_type_lvl2','case_type_lvl3','x_codigo_apertura','x_grupo_trabajo','x_impacto','x_fecha_compromiso_sla','x_fec_cierre','oper_system','incident','incident_xml')