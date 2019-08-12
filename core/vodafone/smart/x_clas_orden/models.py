from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class XClasOrden(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    #dev = models.FloatField(blank=True, null=True)
    x_estado_servicio = models.CharField(max_length=2, blank=True, null=True)
    x_estado_cliente = models.CharField(max_length=20, blank=True, null=True)
    x_clasificacion = models.CharField(max_length=20, blank=True, null=True)
    x_rgu_telf = models.CharField(max_length=1, blank=True, null=True)
    x_tipo_cliente = models.CharField(max_length=2, blank=True, null=True)
    x_tipo_orden = models.CharField(max_length=3, blank=True, null=True)
    x_modify_stamp = models.DateTimeField(blank=True, null=True)
    x_qcode = models.CharField(max_length=2, blank=True, null=True)
    x_subtipo_cliente = models.CharField(max_length=2, blank=True, null=True)
    x_servicio_marca = models.CharField(max_length=5, blank=True, null=True)
    x_peso = models.CharField(max_length=1, blank=True, null=True)
    x_franquicia = models.CharField(max_length=7, blank=True, null=True)
    x_rgu_cm = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_tp = models.CharField(max_length=1, blank=True, null=True)
    x_id_process1 = models.CharField(max_length=50, blank=True, null=True)
    x_id_process2 = models.CharField(max_length=50, blank=True, null=True)
    x_descripcion = models.CharField(max_length=80, blank=True, null=True)
    x_division = models.CharField(max_length=2, blank=True, null=True)
    x_clase = models.CharField(max_length=1, blank=True, null=True)
    x_serv_padre = models.CharField(max_length=50, blank=True, null=True)
    x_rgu_dtv = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_catv = models.CharField(max_length=1, blank=True, null=True)
    x_id_process3 = models.CharField(max_length=50, blank=True, null=True)
    x_id_process4 = models.CharField(max_length=50, blank=True, null=True)
    x_puntos = models.FloatField(blank=True, null=True)
    x_rgu_ri = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_rdsi = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_relacionada = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_sae = models.CharField(max_length=2, blank=True, null=True)
    x_servicio_marca1 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_marca2 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_marca3 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_marca4 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_reconexion2 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_reconexion3 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_reconexion4 = models.CharField(max_length=5, blank=True, null=True)
    x_tipo_cierre_orden = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_ai = models.CharField(max_length=1, blank=True, null=True)
    x_servicio_reconexion1 = models.CharField(max_length=5, blank=True, null=True)
    x_check_in = models.CharField(max_length=1, blank=True, null=True)
    x_clasif_adicional = models.CharField(max_length=20, blank=True, null=True)
    x_tipo_cierre_orden_canc = models.CharField(max_length=1, blank=True, null=True)
    x_tecnologia = models.CharField(max_length=1, blank=True, null=True)
    x_mig_catv = models.CharField(max_length=2, blank=True, null=True)
    x_mig_cm = models.CharField(max_length=2, blank=True, null=True)
    x_mig_dtv = models.CharField(max_length=2, blank=True, null=True)
    x_mig_tf = models.CharField(max_length=2, blank=True, null=True)
    x_id_process5 = models.CharField(max_length=50, blank=True, null=True)
    x_orden_mv = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_mv = models.CharField(max_length=1, blank=True, null=True)
    x_servicio_marca5 = models.CharField(max_length=5, blank=True, null=True)
    x_servicio_reconexion5 = models.CharField(max_length=5, blank=True, null=True)
    x_rgu_rpv = models.CharField(max_length=1, blank=True, null=True)
    x_rgu_adsli = models.CharField(max_length=1, blank=True, null=True)
    x_pvr = models.CharField(max_length=1, blank=True, null=True)
    x_tipo_equipo = models.CharField(max_length=1, blank=True, null=True)
    x_tb = models.CharField(max_length=2, blank=True, null=True)
    x_ip_fija = models.CharField(max_length=2, blank=True, null=True)
    x_amlt = models.CharField(max_length=2, blank=True, null=True)
    x_combinado = models.FloatField(blank=True, null=True)
    x_boxtv = models.CharField(max_length=1, blank=True, null=True)
    x_convergente = models.FloatField(blank=True, null=True)
    x_npvr = models.CharField(max_length=1, blank=True, null=True)
    x_boxtv_npvr = models.CharField(max_length=1, blank=True, null=True)
    x_pm_engine = models.FloatField(blank=True, null=True)
    x_sw = models.CharField(max_length=1, blank=True, null=True)

    def __json_encode__(self):
        output={}
        for field in self._meta.fields:
            output[field.name]=getattr(self, field.name)
        return output   

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_X_CLAS_ORDEN\"'
 
        

