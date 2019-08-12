from core.validation.models import Validation

class VerificacionMovilEquipo:
	def validate(obj):
		from core.exceptions.customexceptions import ApiException
		from core.vodafone.smart import smart_query
		
		try:
		
		    validation=Validation()
		    
		    query_equipos= """ select sp.serial_no, eqMSISDN.x_numero_serie as MSISDN, eqSIM.x_numero_serie as SIM  
		                                        from sa.table_site_part sp
		                                             left join ( sa.table_x_equipos eqMSISDN) on (sp.serial_no=eqMSISDN.x_numero_serie and eqMSISDN.x_estado='5' and eqMSISDN.x_equipo2site=sp.all_site_part2site)
		                                             left join ( sa.table_x_equipos eqSIM) on (eqMSISDN.x_Parent2x_Equipo is not null and eqMSISDN.x_Parent2x_Equipo=eqSIM.objid and eqSIM.x_estado='5' and eqSIM.x_equipo2site=sp.all_site_part2site)
		                                        where sp.all_site_part2site = %s
		                                        and   sp.instance_name in ('MRPD1', 'MPPD2', 'MRPPR')
		                                        and  (sp.part_status <> 'Desconectado' or (sp.service_end_dt = to_date('01/01/1753 00:00:00', 'dd/mm/yyyy HH24:MI:SS') or sp.service_end_dt > sysdate))  """ % (obj.objid)
		                                            
		                                            
		    equipos=smart_query.my_custom_sql('smart_gg', query_equipos)
		    if (len(equipos)!=0):
		        msgs=[]
		        for equipo in equipos:
		            if equipo['msisdn']=='':
		                msgs.append('Servicio %s no esta correctamente asociado a un MSISDN en la tabla de equipos' % equipo['serial_no'])
		            elif equipo['sim']=='':
		                msgs.append('Servicio %s no esta correctamente asociado a una SIM en la tabla de equipos' % equipo['serial_no'])
		            else:
		                pass
		
		        if (len(msgs)!=0):
		            validation.setValues(-1,"Cliente con servicios incorrectamente asociados a equipos", "%s" % ",".join(msgs))
		        else:
		            validation.setValues(0,"OK", "OK")        
		
		    else:
		        validation.setValues(0,"OK", "OK")
		    
		except  Exception as e:
		    validation.setValues(-1,"VerificacionMovilEquipo Exception", str(e))
		
		return validation
