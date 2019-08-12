from core.validation.models import Validation

class TipologiaProductosCliente:
	def validate(obj):
		from core.exceptions.customexceptions import ApiException
		from core.vodafone.smart import smart_query
		
		try:
		
			validation=Validation()
			
			query_CustomerTypologyProducts= """  select *
											from 
											(        
											  SELECT DECODE(datos.x_tipo_cliente, '*', 'VALIDO', CASE WHEN datos.x_tipo_clte=datos.TipoCltePartNum THEN 'VALIDO' ELSE 'NO VALIDO' END) as esValido, datos.*
											  FROM
											  (
											  SELECT pn.x_tipo_cliente, pn.part_number, s.x_tipo_clte, (SELECT x_codigo FROM table_x_pop_up p WHERE p.x_nombre_lista = 'ClaseCliente' and pn.x_tipo_cliente=p.x_des_larga and s.x_tipo_clte =p.x_codigo)  TipoCltePartNum
											  FROM   SA.TABLE_SITE_PART sp,
													 SA.TABLE_MOD_LEVEL ml,
													 SA.TABLE_PART_NUM pn,
													 SA.TABLE_SITE s
											  WHERE  1=1
											  and s.objid=%s
											  and sp.all_site_part2site=s.objid
											  and (sp.part_status <> 'Desconectado' or (sp.service_end_dt = to_date('01/01/1753 00:00:00', 'dd/mm/yyyy HH24:MI:SS') or sp.service_end_dt > sysdate))
											  AND sp.site_part2part_info = ml.objid
											  AND ml.PART_INFO2PART_NUM = pn.objid
											  and pn.part_number not in ('MEGTT')
											  ) datos
											) info
											where info.esValido='NO VALIDO'  """ % (obj.objid)
			
			
			customerTypologyProducts=smart_query.my_custom_sql('smart_gg', query_CustomerTypologyProducts)
			if (len(customerTypologyProducts)!=0):
				validation.setValues(-1,"Clientes con productos incompatibles con la tipologia del cliente", "Clientes con tipologia %s tiene los siguientes productos incompatibles: %s" % (obj.x_tipo_clte, ",".join(list(map(lambda x:x['part_number'],customerTypologyProducts)))))    
			else:
				validation.setValues(0,"OK", "OK")        
			
		except  Exception as e:
			validation.setValues(-1,"TipologiaProductosCliente Exception", str(e))
		
		return validation
