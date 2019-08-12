from core.validation.models import Validation

class ClientePendienteCambio:
	def validate(obj):
		from core.exceptions.customexceptions import ApiException
		from core.vodafone.smart import smart_query
		
		try:
			
		
			validation=Validation()
			
			if (obj.x_estado_cliente!='Pend de Cambio'):
				validation.setValues(0,"OK", "OK")        
			else:    
			
				query_ClientPendingChange= """  select co.objid, co.order_status
												from sa.table_site st, sa.table_contract co, sa.table_contr_schedule cs
												where st.objid = %s 
												and st.x_estado_cliente = 'Pend de Cambio'
												and cs.ship_to2site = st.objid
												and co.objid = cs.schedule2contract
												and co.order_status in ('Abierta', 'Pend de Cancelar')
												Union 
												select co.objid, co.order_status
												from sa.table_site st, sa.table_contract co, sa.table_contr_schedule cs, sa.table_proc_inst pi , sa.table_process pc
												where st.objid = %s 
												and st.x_estado_cliente = 'Pend de Cambio'
												and cs.ship_to2site = st.objid
												and co.objid = cs.schedule2contract
												and co.order_status in ('Cerrada', 'Cancelada', 'Cerrada - No Valida')
												and pi.focus_lowid = co.objid
												and pi.proc_inst2process = pc.objid
												and pi.status <> 'COMPLETE'
												Union
												select co.objid, co.order_status
												from sa.table_site st, sa.table_contract co, sa.table_contr_schedule cs, sa.table_bpm_proc_inst proc
												where st.objid = %s 
												and st.x_estado_cliente = 'Pend de Cambio'
												and cs.ship_to2site = st.objid
												and co.objid = cs.schedule2contract
												and co.order_status in ('Cerrada', 'Cancelada', 'Cerrada - No Valida')
												and proc.focus_objid = co.objid
												and not (((proc.root_status = '0' or proc.root_status = '10') and (proc.status = '10')) or (proc.root_status = '15'))
												and proc.parent2proc_inst is null """ % (obj.objid, obj.objid, obj.objid)
				
				
				clientPendingChange=smart_query.my_custom_sql('smart_gg', query_ClientPendingChange)
				if (len(clientPendingChange)!=0):
					validation.setValues(0,"OK", "OK")        
				else:
					validation.setValues(-1,"Cliente en estado 'Pend de Cambio' sin orden en curso", "Cliente en estado 'Pend de Cambio' sin orden en curso")    
				
			
		except  Exception as e:
			validation.setValues(-1,"ClientePendienteCambio Exception", str(e))    
		
		return validation
		
				
				
