from django.db import models
import django.db.models.options as options
import re
from datetime import datetime
from django.conf import settings
from ApiADA.constantes import Constantes
from xml.etree import ElementTree
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class TableCase(models.Model):

    objid = models.FloatField(primary_key=True)
    title = models.CharField(max_length=80, blank=True, null=True)
    s_title = models.CharField(max_length=80, blank=True, null=True)
    id_number = models.CharField(max_length=255, blank=True, null=True)
    creation_time = models.DateTimeField(blank=True, null=True)
    internal_case = models.FloatField(blank=True, null=True)
    hangup_time = models.DateTimeField(blank=True, null=True)
    alt_phone_num = models.CharField(max_length=20, blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    pickup_ext = models.CharField(max_length=8, blank=True, null=True)
    case_history = models.TextField(blank=True, null=True)
    topics_title = models.CharField(max_length=255, blank=True, null=True)
    yank_flag = models.FloatField(blank=True, null=True)
    server_status = models.CharField(max_length=2, blank=True, null=True)
    support_type = models.CharField(max_length=2, blank=True, null=True)
    warranty_flag = models.CharField(max_length=2, blank=True, null=True)
    support_msg = models.CharField(max_length=80, blank=True, null=True)
    alt_first_name = models.CharField(max_length=30, blank=True, null=True)
    alt_last_name = models.CharField(max_length=30, blank=True, null=True)
    alt_fax_number = models.CharField(max_length=20, blank=True, null=True)
    alt_e_mail = models.CharField(max_length=80, blank=True, null=True)
    alt_site_name = models.CharField(max_length=80, blank=True, null=True)
    alt_address = models.CharField(max_length=200, blank=True, null=True)
    alt_city = models.CharField(max_length=30, blank=True, null=True)
    alt_state = models.CharField(max_length=30, blank=True, null=True)
    alt_zipcode = models.CharField(max_length=20, blank=True, null=True)
    fcs_cc_notify = models.FloatField(blank=True, null=True)
    symptom_code = models.CharField(max_length=10, blank=True, null=True)
    cure_code = models.CharField(max_length=10, blank=True, null=True)
    site_time = models.DateTimeField(blank=True, null=True)
    alt_prod_serial = models.CharField(max_length=30, blank=True, null=True)
    msg_wait_count = models.FloatField(blank=True, null=True)
    reply_wait_count = models.FloatField(blank=True, null=True)
    reply_state = models.FloatField(blank=True, null=True)
    oper_system = models.CharField(max_length=20, blank=True, null=True)
    case_sup_type = models.CharField(max_length=2, blank=True, null=True)
    payment_method = models.CharField(max_length=30, blank=True, null=True)
    ref_number = models.CharField(max_length=80, blank=True, null=True)
    doa_check_box = models.FloatField(blank=True, null=True)
    customer_satis = models.FloatField(blank=True, null=True)
    customer_code = models.CharField(max_length=20, blank=True, null=True)
    service_id = models.CharField(max_length=30, blank=True, null=True)
    alt_phone = models.CharField(max_length=20, blank=True, null=True)
    forward_check = models.FloatField(blank=True, null=True)
    cclist1 = models.CharField(max_length=255, blank=True, null=True)
    cclist2 = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    ownership_stmp = models.DateTimeField(blank=True, null=True)
    modify_stmp = models.DateTimeField(blank=True, null=True)
    dist = models.FloatField(blank=True, null=True)
    arch_ind = models.FloatField(blank=True, null=True)
    is_supercase = models.FloatField(blank=True, null=True)
    dev = models.FloatField(blank=True, null=True)
    case_type_lvl1 = models.CharField(max_length=40, blank=True, null=True)
    case_type_lvl2 = models.CharField(max_length=40, blank=True, null=True)
    case_type_lvl3 = models.CharField(max_length=40, blank=True, null=True)
    x_codigo_apertura = models.CharField(max_length=40, blank=True, null=True)
    x_origen = models.CharField(max_length=40, blank=True, null=True)
    x_tramo_red = models.CharField(max_length=40, blank=True, null=True)
    x_cpo = models.CharField(max_length=30, blank=True, null=True)
    x_elemento_red = models.CharField(max_length=256, blank=True, null=True)
    x_descripcion = models.CharField(max_length=1000, blank=True, null=True)
    x_nserie_telefonica = models.CharField(max_length=40, blank=True, null=True)
    x_tipo_instalacion_red = models.CharField(max_length=50, blank=True, null=True)
    x_causa = models.CharField(max_length=1000, blank=True, null=True)
    x_nlineas = models.FloatField(blank=True, null=True)
    x_lugar_resol = models.CharField(max_length=30, blank=True, null=True)
    x_id_elemento = models.CharField(max_length=50, blank=True, null=True)
    x_avisadotecn = models.CharField(max_length=3, blank=True, null=True)
    x_proveedor = models.CharField(max_length=50, blank=True, null=True)
    x_ambito = models.CharField(max_length=20, blank=True, null=True)
    x_tipo_operacion = models.CharField(max_length=50, blank=True, null=True)
    x_recup_datos = models.CharField(max_length=3, blank=True, null=True)
    x_nuevo_seguridad = models.CharField(max_length=3, blank=True, null=True)
    x_metodo_entrega = models.CharField(max_length=30, blank=True, null=True)
    x_grupo_servicio = models.CharField(max_length=80, blank=True, null=True)
    x_trabajo_especial = models.FloatField(blank=True, null=True)
    x_motivo = models.CharField(max_length=80, blank=True, null=True)
    x_submotivo = models.CharField(max_length=80, blank=True, null=True)
    case_soln2workaround = models.FloatField(blank=True, null=True)
    case_prevq2queue = models.FloatField(blank=True, null=True)
    case_currq2queue = models.FloatField(blank=True, null=True)
    case_wip2wipbin = models.FloatField(blank=True, null=True)
    case_logic2prog_logic = models.FloatField(blank=True, null=True)
    case_owner2user = models.FloatField(blank=True, null=True)
    case_state2condition = models.FloatField(blank=True, null=True)
    case_originator2user = models.FloatField(blank=True, null=True)
    case_empl2employee = models.FloatField(blank=True, null=True)
    calltype2gbst_elm = models.FloatField(blank=True, null=True)
    respprty2gbst_elm = models.FloatField(blank=True, null=True)
    respsvrty2gbst_elm = models.FloatField(blank=True, null=True)
    case_prod2site_part = models.FloatField(blank=True, null=True)
    case_reporter2site = models.FloatField(blank=True, null=True)
    case_reporter2contact = models.FloatField(blank=True, null=True)
    entitlement2contract = models.FloatField(blank=True, null=True)
    casests2gbst_elm = models.FloatField(blank=True, null=True)
    case_rip2ripbin = models.FloatField(blank=True, null=True)
    covrd_ppi2site_part = models.FloatField(blank=True, null=True)
    case_distr2site = models.FloatField(blank=True, null=True)
    case2address = models.FloatField(blank=True, null=True)
    case_node2site_part = models.FloatField(blank=True, null=True)
    de_product2site_part = models.FloatField(blank=True, null=True)
    case_prt2part_info = models.FloatField(blank=True, null=True)
    de_prt2part_info = models.FloatField(blank=True, null=True)
    alt_contact2contact = models.FloatField(blank=True, null=True)
    task2opportunity = models.FloatField(blank=True, null=True)
    case2life_cycle = models.FloatField(blank=True, null=True)
    case_victim2case = models.FloatField(blank=True, null=True)
    entitle2contr_itm = models.FloatField(blank=True, null=True)
    case2blg_argmnt = models.FloatField(blank=True, null=True)
    case2fin_accnt = models.FloatField(blank=True, null=True)
    case2pay_channel = models.FloatField(blank=True, null=True)
    case2x_seguim_accion = models.FloatField(blank=True, null=True)
    case2order = models.FloatField(blank=True, null=True)
    x_codigo_red_ggcc = models.CharField(max_length=40, blank=True, null=True)
    x_grp_servicio_emp = models.CharField(max_length=128, blank=True, null=True)
    x_tipo_comerciabilidad = models.CharField(max_length=5, blank=True, null=True)
    x_cobertura_cpo = models.CharField(max_length=40, blank=True, null=True)
    x_grupo_ttp = models.CharField(max_length=40, blank=True, null=True)
    x_niv_aprob_ttp = models.CharField(max_length=40, blank=True, null=True)
    x_subgrupo_ttp = models.CharField(max_length=40, blank=True, null=True)
    x_zona_ono = models.CharField(max_length=40, blank=True, null=True)
    x_serv_afec_recl = models.CharField(max_length=40, blank=True, null=True)
    case2transn_map = models.FloatField(blank=True, null=True)
    case2pp_bucket = models.FloatField(blank=True, null=True)
    x_ccc = models.CharField(max_length=10, blank=True, null=True)
    case_reporter2bus_org = models.FloatField(blank=True, null=True)
    alt_bus_org2bus_org = models.FloatField(blank=True, null=True)
    alt_address2address = models.FloatField(blank=True, null=True)
    case2subscript_ref = models.FloatField(blank=True, null=True)
    case2blg_arg_ref = models.FloatField(blank=True, null=True)
    case2prepay_acct_ref = models.FloatField(blank=True, null=True)
    case2cust_acct_ref = models.FloatField(blank=True, null=True)
    case_lvl12hgbst_elm = models.FloatField(blank=True, null=True)
    case_lvl22hgbst_elm = models.FloatField(blank=True, null=True)
    case_lvl32hgbst_elm = models.FloatField(blank=True, null=True)
    x_desc_averia = models.CharField(max_length=512, blank=True, null=True)
    x_acciones_tecnico = models.CharField(max_length=512, blank=True, null=True)
    x_cod_equipo = models.CharField(max_length=20, blank=True, null=True)
    x_causa_fallo = models.CharField(max_length=40, blank=True, null=True)
    x_num_repetidas = models.CharField(max_length=20, blank=True, null=True)
    x_num_anterior = models.CharField(max_length=255, blank=True, null=True)
    x_fecha_disponible = models.DateTimeField(blank=True, null=True)
    x_inter_disp = models.FloatField(blank=True, null=True)
    x_argumentario = models.CharField(max_length=1, blank=True, null=True)
    x_origen2 = models.CharField(max_length=40, blank=True, null=True)
    x_flujo_vpt = models.FloatField(blank=True, null=True)
    x_sm_rma = models.CharField(max_length=20, blank=True, null=True)
    x_codigo_sap = models.CharField(max_length=20, blank=True, null=True)
    x_sc_origen = models.CharField(max_length=1, blank=True, null=True)
    x_case2lite_proc_inst = models.CharField(max_length=31, blank=True, null=True)
    x_fecha_prevista = models.DateTimeField(blank=True, null=True)
    x_codificacion = models.CharField(max_length=7, blank=True, null=True)
    x_numero = models.FloatField(blank=True, null=True)
    x_id_solicitud = models.CharField(max_length=50, blank=True, null=True)
    x_sc2_id_destino = models.CharField(max_length=40, blank=True, null=True)
    x_sc2_tipo_tras_reco = models.CharField(max_length=50, blank=True, null=True)
    x_sc2_opc_dispatch = models.CharField(max_length=20, blank=True, null=True)
    x_tipo_2 = models.CharField(max_length=40, blank=True, null=True)
    x_tipo_3 = models.CharField(max_length=40, blank=True, null=True)
    x_imp_reclamado = models.CharField(max_length=10, blank=True, null=True)
    x_id_administrativo = models.CharField(max_length=50, blank=True, null=True)
    x_num_clte_bs_potencial = models.FloatField(blank=True, null=True)
    x_sistema_afectado = models.CharField(max_length=20, blank=True, null=True)
    x_cierre_manual = models.FloatField(blank=True, null=True)
    x_grupo_trabajo = models.CharField(max_length=80, blank=True, null=True)
    x_fec_cierre_conf = models.DateTimeField(blank=True, null=True)
    x_fec_max_conf = models.DateTimeField(blank=True, null=True)
    x_fec_solucion = models.DateTimeField(blank=True, null=True)
    x_horario_contacto = models.CharField(max_length=80, blank=True, null=True)
    x_flag_reloj = models.FloatField(blank=True, null=True)
    x_impacto = models.CharField(max_length=90, blank=True, null=True)
    x_fecha_reanudacion = models.DateTimeField(blank=True, null=True)
    x_motivo_parada = models.CharField(max_length=90, blank=True, null=True)
    case2x_inter_estados = models.FloatField(blank=True, null=True)
    x_id_ticket_remedy = models.CharField(max_length=15, blank=True, null=True)
    x_fecha_compromiso_sla = models.DateTimeField(blank=True, null=True)
    x_intervalo_sla = models.FloatField(blank=True, null=True)
    x_sla_enviado = models.FloatField(blank=True, null=True)
    x_ticket_resolved = models.FloatField(blank=True, null=True)
    x_deteccion = models.CharField(max_length=40, blank=True, null=True)
    x_motivo_modif_sla = models.CharField(max_length=28, blank=True, null=True)
    x_fec_cierre = models.DateTimeField(blank=True, null=True)
    x_chk_seguimiento = models.FloatField(blank=True, null=True)
    x_imputacion = models.CharField(max_length=80, blank=True, null=True)
    x_fecha_aviso = models.DateTimeField(blank=True, null=True)
    x_estado_tesa = models.CharField(max_length=80, blank=True, null=True)
    x_fecha_cmb_est_tesa = models.DateTimeField(blank=True, null=True)
    x_num_reintentos_llamada = models.FloatField(blank=True, null=True)
    x_persona_contacto = models.CharField(max_length=30, blank=True, null=True)
    x_perf_aprob_ini = models.CharField(max_length=30, blank=True, null=True)
    x_canal = models.CharField(max_length=80, blank=True, null=True)
    x_id_ticket_ipm = models.CharField(max_length=15, blank=True, null=True)
    x_mail_contacto = models.CharField(max_length=80, blank=True, null=True)
    x_grupo_responsable = models.CharField(max_length=20, blank=True, null=True)
    x_reiterada = models.FloatField(blank=True, null=True)
    x_agencia_ajuste = models.CharField(max_length=50, blank=True, null=True)
    x_of_venta_ajuste = models.CharField(max_length=50, blank=True, null=True)
    x_forma_pago_ajuste = models.CharField(max_length=15, blank=True, null=True)
    x_impacto_rem = models.CharField(max_length=60, blank=True, null=True)
    x_urgencia_rem = models.CharField(max_length=60, blank=True, null=True)
    x_login_gestor = models.CharField(max_length=40, blank=True, null=True)
    x_proveedor_co = models.CharField(max_length=40, blank=True, null=True)
    x_service_id = models.CharField(max_length=80, blank=True, null=True)
    x_codigo_resol_1 = models.CharField(max_length=40, blank=True, null=True)
    x_codigo_resol_2 = models.CharField(max_length=40, blank=True, null=True)
    x_codigo_resol_3 = models.CharField(max_length=40, blank=True, null=True)
    x_status_reson = models.CharField(max_length=40, blank=True, null=True)
    x_gt_owner = models.CharField(max_length=80, blank=True, null=True)
    x_ows = models.CharField(max_length=10, blank=True, null=True)
    x_num_telf = models.CharField(max_length=9, blank=True, null=True)
    x_ot_afectada = models.CharField(max_length=20, blank=True, null=True)
    x_old_status = models.CharField(max_length=80, blank=True, null=True)
    x_ticket_ext_tesa = models.CharField(max_length=50, blank=True, null=True)
    x_cod_incidencia = models.CharField(max_length=40, blank=True, null=True)

    @property
    def incident(self):
        try:
            inc_regex=re.compile('INC.*?-|PBI.*?-', re.I | re.M)
            matches=inc_regex.findall(self.title)
            if (len(matches)>0):
                return matches[0][0:-1].strip()  
            else:
                return self.incident_xml    
        except:
            return None


        

    @property
    def incident_xml(self):  
        try:
            xml_regex=re.compile('<info>.*?<\/info>', re.I | re.M)
            matches=xml_regex.findall(self.case_history)
            if (len(matches)>0):
                case_xml=matches[-1]  
                doc=ElementTree.fromstring(case_xml.upper())
                return doc.find("./PARAMETRO[NAME='INC_REMEDY']/VALUE").text.strip()
            else:
                return None    
        except:
            return None


    def __json_encode__(self):
        output={}
        for field in self._meta.fields:
            output[field.name]=getattr(self, field.name)
        return output  

    def getCommentsWorklog(self):

        text=self.case_history.replace('\r','\n')
        miregex=re.compile('\*\*\* .* (?P<date>[0-9]+\/[0-9]+\/[0-9]+ [0-9]+:[0-9]+:[0-9]+) .*', re.I )
        #miregex=re.compile('\*\*\* (?:\w(?:\s|\w)*) (?P<date>[0-9]{2}\/[0-9]{2}\/[0-9]{4} [0-9]{2}:[0-9]{2}:[0-9]{2}) .*', re.I)
        comments_regex=[]
        for m in miregex.finditer(text):    
            comment_info={"start":m.start(), "date": m.group(1)}
            comments_regex.append(comment_info)
        
        comments=[]
        if (len(comments_regex)>0):
            comment={}
            start_position=comments_regex[0]['start']
            #comment["date"]=comments_regex[0]['date']
            try:
                comment["date"]=datetime.strptime(comments_regex[0]['date'],'%d/%m/%Y %H:%M:%S').strftime(Constantes.DATETIME_FORMAT)
            except:
                comment["date"]=datetime.strptime(comments_regex[0]['date'],'%m/%d/%Y %H:%M:%S').strftime(Constantes.DATETIME_FORMAT)



            #Creo que esto debería de ser i=0
            i=1
            while i<len(comments_regex):
                comment["text"]=text[start_position:comments_regex[i]['start']]
                comments.append(comment)
                comment={}
                start_position=comments_regex[i]['start']
                #comment["date"]=comments_regex[i]['date']
                try:
                    comment["date"]=datetime.strptime(comments_regex[i]['date'],'%d/%m/%Y %H:%M:%S').strftime(Constantes.DATETIME_FORMAT)
                except:
                    comment["date"]=datetime.strptime(comments_regex[i]['date'],'%m/%d/%Y %H:%M:%S').strftime(Constantes.DATETIME_FORMAT)
                i+=1
            comment["text"]=text[start_position:]
            comments.append(comment)
        
        return comments

    class Meta:
        in_db = 'smart_gg'
        managed = False
        db_table = '\"SA\".\"TABLE_CASE\"'
