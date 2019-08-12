from core.validation.models import Validation

class InstanciasDuplicadas:
	def validate(obj):
		from core.exceptions.customexceptions import ApiException
		from core.vodafone.smart import smart_query
		
		validation=Validation()
		try:
			
		
		
			query_duplicateinstance= """ select sp.x_seq_instance 
										 from sa.table_site_part sp 
										 where sp.all_site_part2site = %s
										 and  (sp.part_status <> 'Desconectado' or (sp.service_end_dt = to_date('01/01/1753 00:00:00', 'dd/mm/yyyy HH24:MI:SS') or sp.service_end_dt > sysdate))
										 group by sp.x_seq_instance
										 having count(*) > 1 """ % (obj.objid)
			
			
		
			xSeqInstance=smart_query.my_custom_sql('smart_gg', query_duplicateinstance)
			if (len(xSeqInstance)==0):
				validation.setValues(0,"OK", "OK")		
			else:
				validation.setValues(-1,"Clientes con instancias duplicadas en parque", "Clientes con instancias duplicadas en parque: %s" % ",".join(list(map(lambda x:x['x_seq_instance'],xSeqInstance))))	
			
		
		except  Exception as e:
			validation.setValues(-1,"InstanciasDuplicadas Exception", str(e))	
		return validation
		
