from django.db import models
import django.db.models.options as options
from core.vodafone.smart.user.models import User
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

# Create your models here.

class Contract(models.Model):

    objid = models.FloatField(blank=True, primary_key=True)
    id = models.CharField(max_length=40, blank=True, null=True)
    s_id = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    po_number = models.CharField(max_length=40, blank=True, null=True)
    s_po_number = models.CharField(max_length=40, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    expire_date = models.DateTimeField(blank=True, null=True)
    unit_type = models.CharField(max_length=30, blank=True, null=True)
    units_purch = models.FloatField(blank=True, null=True)
    units_used = models.FloatField(blank=True, null=True)
    units_avail = models.FloatField(blank=True, null=True)
    phone_resp = models.FloatField(blank=True, null=True)
    onsite_resp = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)
    hours_for_pm = models.CharField(max_length=30, blank=True, null=True)
    spec_consid = models.FloatField(blank=True, null=True)
    pay_options = models.CharField(max_length=30, blank=True, null=True)
    alert_ind = models.FloatField(blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    q_start_date = models.DateTimeField(blank=True, null=True)
    quote_dur = models.FloatField(blank=True, null=True)
    terms_cond = models.CharField(max_length=40, blank=True, null=True)
    contr_dur = models.CharField(max_length=40, blank=True, null=True)
    renew_prior = models.FloatField(blank=True, null=True)
    total_tax_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total_net = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    total_gross = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    arch_ind = models.FloatField(blank=True, null=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    s_title = models.CharField(max_length=80, blank=True, null=True)
    q_end_date = models.DateTimeField(blank=True, null=True)
    evergreen_ind = models.FloatField(blank=True, null=True)
    renew_notf_ind = models.FloatField(blank=True, null=True)
    sched_ind = models.FloatField(blank=True, null=True)
    fsvc_end_date = models.DateTimeField(blank=True, null=True)
    close_eff_dt = models.DateTimeField(blank=True, null=True)
    close_crdt_ind = models.FloatField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    last_xfer = models.DateTimeField(blank=True, null=True)
    q_issue_dt = models.DateTimeField(blank=True, null=True)
    warr_set_ind = models.FloatField(blank=True, null=True)
    dflt_start_dt = models.DateTimeField(blank=True, null=True)
    dflt_end_dt = models.DateTimeField(blank=True, null=True)
    renew_ntfy_dt = models.DateTimeField(blank=True, null=True)
    ready_to_bill = models.FloatField(blank=True, null=True)
    struct_type = models.FloatField(blank=True, null=True)
    create_dt = models.DateTimeField(blank=True, null=True)
    dev = models.FloatField(blank=True, null=True)
    tot_ship_amt = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    last_save_dt = models.DateTimeField(blank=True, null=True)
    ord_submit_dt = models.DateTimeField(blank=True, null=True)
    handling_cost = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    order_status = models.CharField(max_length=30, blank=True, null=True)
    x_estado = models.CharField(max_length=40, blank=True, null=True)
    x_funnel = models.CharField(max_length=10, blank=True, null=True)
    #owner2user = models.FloatField(blank=True, null=True)
    owner2user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='owner2user', related_name='owner2user')
    contract2condition = models.FloatField(blank=True, null=True)
    status2gbst_elm = models.FloatField(blank=True, null=True)
    contract2currency = models.FloatField(blank=True, null=True)
    contract2admin = models.FloatField(blank=True, null=True)
    #contr_originator2user = models.FloatField(blank=True, null=True)
    contr_originator2user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='contr_originator2user', related_name='contr_originator2user')
    contr_prevq2queue = models.FloatField(blank=True, null=True)
    contr_currq2queue = models.FloatField(blank=True, null=True)
    contr_wip2wipbin = models.FloatField(blank=True, null=True)
    primary2contact = models.FloatField(blank=True, null=True)
    sell_to2bus_org = models.FloatField(blank=True, null=True)
    contr_quote2opportunity = models.FloatField(blank=True, null=True)
    contract2price_prog = models.FloatField(blank=True, null=True)
    x_campana = models.CharField(max_length=3, blank=True, null=True)
    x_cod_razoncancela = models.CharField(max_length=80, blank=True, null=True)
    x_cod_razonvendedor = models.CharField(max_length=2, blank=True, null=True)
    x_compania = models.CharField(max_length=2, blank=True, null=True)
    x_des_razonvendedor = models.CharField(max_length=80, blank=True, null=True)
    x_des_vendedor = models.CharField(max_length=80, blank=True, null=True)
    x_estado_excepcion = models.CharField(max_length=2, blank=True, null=True)
    x_fec_venta = models.DateTimeField(blank=True, null=True)
    x_fecha_ini_factura = models.DateTimeField(blank=True, null=True)
    x_fecha_instalador = models.DateTimeField(blank=True, null=True)
    x_fecha_plan = models.DateTimeField(blank=True, null=True)
    x_puntos = models.FloatField(blank=True, null=True)
    x_qcode = models.CharField(max_length=2, blank=True, null=True)
    x_tipo_orden = models.CharField(max_length=3, blank=True, null=True)
    x_tipo_vendedor = models.CharField(max_length=2, blank=True, null=True)
    x_contract2x_clas_orden = models.FloatField(blank=True, null=True)
    contract2lotes = models.FloatField(blank=True, null=True)
    contract2x_puntos = models.FloatField(blank=True, null=True)
    contract2x_slot = models.FloatField(blank=True, null=True)
    contract2x_tecnicos = models.FloatField(blank=True, null=True)
    x_contract2ult_excep = models.FloatField(blank=True, null=True)
    x_contract2ult_plan = models.FloatField(blank=True, null=True)
    x_contract2ult_tecnico = models.FloatField(blank=True, null=True)
    x_instalador2tecnico = models.FloatField(blank=True, null=True)
    x_ult_instal2tecnico = models.FloatField(blank=True, null=True)
    x_vendedor2tecnico = models.FloatField(blank=True, null=True)
    x_child_contract2contract = models.FloatField(blank=True, null=True)
    x_instalac_prod_site = models.FloatField(blank=True, null=True)
    x_contract2x_ing_cliente = models.FloatField(blank=True, null=True)
    x_child_contract_ull2contract = models.FloatField(blank=True, null=True)
    x_franja_horaria = models.CharField(max_length=2, blank=True, null=True)
    x_cent_terr_comercial = models.CharField(max_length=40, blank=True, null=True)
    x_cod_proyecto = models.CharField(max_length=40, blank=True, null=True)
    x_fecha_activacion = models.DateTimeField(blank=True, null=True)
    x_fecha_fin_prov_pinc = models.DateTimeField(blank=True, null=True)
    x_fecha_ini_prov_pinc = models.DateTimeField(blank=True, null=True)
    x_id_oferta = models.CharField(max_length=40, blank=True, null=True)
    x_motivo_baja = models.CharField(max_length=255, blank=True, null=True)
    x_numero_contrato = models.CharField(max_length=40, blank=True, null=True)
    x_numero_pedido = models.CharField(max_length=40, blank=True, null=True)
    x_observaciones = models.CharField(max_length=255, blank=True, null=True)
    x_permiso_instalacion = models.CharField(max_length=15, blank=True, null=True)
    x_resp_comercial = models.CharField(max_length=40, blank=True, null=True)
    x_tecnologia = models.CharField(max_length=30, blank=True, null=True)
    x_viabilidad = models.CharField(max_length=40, blank=True, null=True)
    x_canal = models.CharField(max_length=20, blank=True, null=True)
    x_contract2x_ult_autoriza_inst = models.FloatField(blank=True, null=True)
    x_fecha_vc = models.DateTimeField(blank=True, null=True)
    x_superoferta = models.CharField(max_length=20, blank=True, null=True)
    x_fecha_compromiso = models.DateTimeField(blank=True, null=True)
    x_sla = models.FloatField(blank=True, null=True)
    x_penaliza_na = models.CharField(max_length=80, blank=True, null=True)
    x_fecha_reconexion = models.DateTimeField(blank=True, null=True)
    tot_adj = models.FloatField(blank=True, null=True)
    last_line_num = models.FloatField(blank=True, null=True)
    is_immediate = models.FloatField(blank=True, null=True)
    sub_total = models.FloatField(blank=True, null=True)
    is_created_on_classic = models.FloatField(blank=True, null=True)
    is_single_unit = models.FloatField(blank=True, null=True)
    contract2jpdy_group = models.FloatField(blank=True, null=True)
    bill_to2site = models.FloatField(blank=True, null=True)
    bill_to2contact = models.FloatField(blank=True, null=True)
    dealer_code2hgbst_elm = models.FloatField(blank=True, null=True)
    contract2sale_channl = models.FloatField(blank=True, null=True)
    x_imp_carta = models.FloatField(blank=True, null=True)
    x_no_envio = models.CharField(max_length=1, blank=True, null=True)
    x_padre = models.CharField(max_length=2, blank=True, null=True)
    x_id_padre = models.CharField(max_length=25, blank=True, null=True)
    x_ticket_baja = models.CharField(max_length=255, blank=True, null=True)
    contract2boh_be = models.FloatField(blank=True, null=True)
    order2customer = models.FloatField(blank=True, null=True)
    cont_term2hgbst_elm = models.FloatField(blank=True, null=True)
    cont_type2hgbst_elm = models.FloatField(blank=True, null=True)
    x_autoasig_bam = models.CharField(max_length=1, blank=True, null=True)
    x_autoinstalable = models.CharField(max_length=1, blank=True, null=True)
    x_autoinstalacion = models.CharField(max_length=1, blank=True, null=True)
    x_perfil_autoinstalacion = models.CharField(max_length=1, blank=True, null=True)
    x_tipo_asig_esen = models.CharField(max_length=1, blank=True, null=True)
    x_web_ecare = models.CharField(max_length=30, blank=True, null=True)
    contract2x_tecnicos_p = models.FloatField(blank=True, null=True)
    x_flujo_inst = models.CharField(max_length=50, blank=True, null=True)
    x_rec_tarj = models.FloatField(blank=True, null=True)
    x_sc_origen = models.CharField(max_length=1, blank=True, null=True)
    x_diferido_ciclo = models.CharField(max_length=2, blank=True, null=True)
    x_pte_port_inversa = models.CharField(max_length=1, blank=True, null=True)
    x_fch_limite_cnc_portab = models.DateTimeField(blank=True, null=True)
    x_autocancel_port = models.FloatField(blank=True, null=True)
    x_seqenvio48h = models.CharField(max_length=9, blank=True, null=True)
    x_red_movil = models.CharField(max_length=30, blank=True, null=True)
    x_orden_comb = models.CharField(max_length=40, blank=True, null=True)
    x_rec_ont = models.FloatField(blank=True, null=True)
    x_rec_bbr = models.FloatField(blank=True, null=True)
    x_id_remoto = models.CharField(max_length=50, blank=True, null=True)
    x_id_administrativo = models.CharField(max_length=50, blank=True, null=True)
    contract2x_cust_order = models.FloatField(blank=True, null=True)
    x_rec_bbc = models.FloatField(blank=True, null=True)
    x_motivo = models.CharField(max_length=255, blank=True, null=True)
    x_quality_check = models.FloatField(blank=True, null=True)
    x_motivo_cv = models.CharField(max_length=40, blank=True, null=True)
    x_submotivo_cv = models.CharField(max_length=40, blank=True, null=True)
    x_mail_envio = models.CharField(max_length=80, blank=True, null=True)
    x_sms_envio = models.CharField(max_length=20, blank=True, null=True)
    x_ciclo_traslado = models.CharField(max_length=1, blank=True, null=True)
    x_cpp_transf = models.CharField(max_length=1, blank=True, null=True)
    x_motivo_transf = models.CharField(max_length=30, blank=True, null=True)
    x_cargo_transf = models.CharField(max_length=1, blank=True, null=True)
    x_etiqueta_orden = models.CharField(max_length=255, blank=True, null=True)
    x_flag_ot_retencion = models.CharField(max_length=2, blank=True, null=True)
    x_no_envio_correos = models.CharField(max_length=1, blank=True, null=True)
    x_nls = models.CharField(max_length=5, blank=True, null=True)
    x_acepta_contrato = models.CharField(max_length=20, blank=True, null=True)
    x_estado_acepta_contrato = models.CharField(max_length=20, blank=True, null=True)
    x_fecha_acepta_contrato = models.DateTimeField(blank=True, null=True)
    x_entrega_tienda = models.CharField(max_length=1, blank=True, null=True)
    #ddd_x_modelo_cesion = models.CharField(max_length=2, blank=True, null=True)
    #ddd_x_contrato_generado = models.CharField(max_length=1, blank=True, null=True)
    x_telefono = models.CharField(max_length=40, blank=True, null=True)
    x_cambio_clase = models.CharField(max_length=30, blank=True, null=True)
    x_contrato_generado = models.CharField(max_length=1, blank=True, null=True)
    x_contrato_impreso = models.CharField(max_length=1, blank=True, null=True)
    x_contract2x_ord_esp = models.FloatField(blank=True, null=True)
    x_modelo_cesion = models.CharField(max_length=2, blank=True, null=True)
    x_gt_crea_ot = models.CharField(max_length=80, blank=True, null=True)
    x_orden_prepago = models.CharField(max_length=1, blank=True, null=True)
    x_alta_ref = models.FloatField(blank=True, null=True)
    x_resp_baja_sgp = models.CharField(max_length=10, blank=True, null=True)
    x_inst_acometida = models.CharField(max_length=5, blank=True, null=True)
    x_id_lead = models.CharField(max_length=15, blank=True, null=True)
    x_grupo_servicios = models.CharField(max_length=30, blank=True, null=True)
    x_comunicacion_tecnico = models.CharField(max_length=80, blank=True, null=True)
    x_tecnologia_ins_mig = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_CONTRACT\"'

