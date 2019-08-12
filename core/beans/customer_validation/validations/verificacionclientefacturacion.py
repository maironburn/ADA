from core.validation.models import Validation

class VerificacionClienteFacturacion:
	def validate(obj):
		from core.exceptions.customexceptions import ApiException
		from core.vodafone.smart import smart_query
		
		try:
		
		    validation=Validation()
		    
		    query_clienteNoPotencial= """ select count(*) from sa.table_site_part sp, sa.table_site st
							   where st.objid = %s
							   and sp.all_site_part2site = st.objid
							   and (sp.part_status <> 'Desconectado' or (sp.service_end_dt = to_date('01/01/1753 00:00:00', 'dd/mm/yyyy HH24:MI:SS') or sp.service_end_dt > sysdate))  """ % (obj.objid)
		                                            
		                                            
		    clienteNoPotencial=smart_query.my_custom_sql('smart_gg', query_clienteNoPotencial)
		    if (len(clienteNoPotencial)!=0):
		        
		        query_tipoCliente= """   SELECT  DC.OBJID,S.SITE_ID ,DC.X_TIPO_AUX
												FROM SA.TABLE_CONTACT_ROLE CR, SA.TABLE_CONTACT C ,SA.TABLE_SITE S, SA.TABLE_X_DETALLE_CONTACTO DC
												WHERE CR.S_ROLE_NAME = 'TITULAR' 
												AND CR.X_CONTACT_TYPE = 'C' 
												AND CR.CONTACT_ROLE2SITE = NVL(S.X_CHILD_SITE2X_SITE, S.OBJID) 
												AND CR.CONTACT_ROLE2CONTACT = C.OBJID 
												AND C.CONTACT2X_DET_CONTACTO = DC.OBJID(+) 
												AND S.OBJID = %s  """ % (obj.objid)
		  
		        tipoCliente=smart_query.my_custom_sql('smart_gg', query_tipoCliente)
		        if (len(tipoCliente)==1):
		            if ((tipoCliente[0]['x_tipo_aux']) and (tipoCliente[0]['x_tipo_aux']!='') and (tipoCliente[0]["x_tipo_aux"] != "OB") and (tipoCliente[0]["x_tipo_aux"] != "EO") and (tipoCliente[0]["x_tipo_aux"] != "EE")):
		                validation.setValues(-1,"El cliente no es ONO, no puede facturar MsjDetallado: Cliente con tipo de contacto incorrecto", "El cliente no es ONO, no puede facturar MsjDetallado: Cliente con tipo de contacto incorrecto")
		            else:
		                validation.setValues(0,"OK", "OK")
		        elif (len(tipoCliente)> 1):
		            validation.setValues(-1,"El cliente no es ONO, no puede facturar MsjDetallado: Cliente con mas de un contacto", "El cliente no es ONO, no puede facturar MsjDetallado: Cliente con mas de un contacto")
		        else:
		            validation.setValues(-1,"El cliente no es ONO, no puede facturar MsjDetallado: No hay informacion de contacto", "El cliente no es ONO, no puede facturar MsjDetallado: No hay informacion de contacto")
		    else:
		        validation.setValues(0,"OK", "OK")
		    
		except  Exception as e:
		    validation.setValues(-1,"VerificacionClienteFacturacion Exception", str(e))
		
		return validation
