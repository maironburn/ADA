from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from appparameter.models import Appparameter
from core.vodafone.smart.contract.models import Contract
from core.vodafone.smart.x_clas_orden.models import XClasOrden
from core.beans.analysis_processinstancecomb.analysis_processinstancecomb import AnalysisProcessInstanceComb
from core.beans.analysis_onolog.analysis_onolog import AnalysisOnolog
import traceback
import json
import datetime
from json_tricks import dumps
from ApiADA.constantes import Constantes
from core.vodafone.smart import smart_query

from core.beans.rules_engine.ruleset import RulesetImplementation
from ruleset.models import Ruleset

log = logging.getLogger(__name__)

class AnalysisContract:

    def analyze(parameters) :

        try:
            log.info('Start: analyze')

            event={}

            if ((not parameters) or (not 'contract' in parameters) or (parameters['contract'] is None) or (parameters['contract'].strip()=='')):
                raise ApiException("Invalid parameters.")

            contract=parameters['contract']    

            try:
                event['contract']=Contract.objects.get(s_id=contract)
                log.info('Analizing contract:' + contract)
                if (event['contract'].order_status!="Cerrada - No Valida"):
                    event['motor']=AnalysisContract.getMOTOR(event['contract'])
                    log.info('Contract Found:' + contract)
                    event['contract_info']=AnalysisContract.getProcessInfo(event['contract'], event['motor'])
                
                AnalysisContract.clasifyContract(event)


            except Contract.DoesNotExist:    
                event['contract']='Contract NOT Found'

            log.info('End: analyze: event:'+dumps(event))
            
            return event

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

    #   inputs:
    #       contract: Objeto con la información de la tabla contract
    #   output:
    #       return un literal con el valor del motor por el que se ha lanzado la orden (APM/CMP)
    # 
    def getMOTOR(contract):        
        log.info('Start: getMOTOR')


        query_processes_cpm="""select count(*) as numprocess
                            from  sa.table_proc_inst pi  
                            where  pi.focus_lowid = %s  
                            and    pi.focus_type = 86 """  % (contract.objid)  #focus_type igual a 86 e sun valor fijo

        query_processes_apm="""select count(*) as numprocess
                            from  sa.table_bpm_proc_inst pi 
                            where  pi.focus_objid = %s  
                            and pi.focus_table_num = 86 """  % (contract.objid) #focus_type igual a 86 e sun valor fijo


        processes=smart_query.my_custom_sql('smart_gg', query_processes_apm)
        data_process=processes[0]
        if (data_process['numprocess']>0):
            log.info('End: getMOTOR')
            return Constantes.MOTOR_ORDER_APM
        else:
            processes=smart_query.my_custom_sql('smart_gg', query_processes_cpm)
            data_process=processes[0]
            if (data_process['numprocess']>0):
                log.info('End: getMOTOR')
                return Constantes.MOTOR_ORDER_CPM
            else:    
                try:
                    xclasorden=XClasOrden.objects.get(objid=contract.x_contract2x_clas_orden)
                    if xclasorden.x_pm_engine == 1:
                        log.info('End: getMOTOR')
                        return Constantes.MOTOR_ORDER_APM
                    else:
                        log.info('End: getMOTOR')
                        return Constantes.MOTOR_ORDER_CPM
        
                except XClasOrden.DoesNotExist: 
                    log.info('End: getMOTOR')   
                    return Constantes.MOTOR_ORDER_CPM
    
    #   inputs:
    #       contract: Objeto con la información de la tabla contract
    #       motor: Objeto del motor por el que se ha lanzado la orden
    #   output:
    #       return el objeto "processInfo" que contiene un diccionario con la información obtenida de la orden
    # 
    def getProcessInfo(contract, motor):
        log.info('Start: getProcessInfo')
       
        if motor == Constantes.MOTOR_ORDER_APM:
            log.info('End: getProcessInfo')
            return AnalysisContractAPM.getProcessInfo(contract)
        else:
            log.info('End: getProcessInfo')
            return AnalysisContractCPM.getProcessInfo(contract)
            

    #####################################################################
    #   inputs:
    #       event: Objeto con el evento, que contiene toda la informacion
    #   output:
    #       return Devuelve alalisis final de la orden
    # 
    #####################################################################
    def clasifyContract(event):
        log.info('Start: clasifyContract')
        
        #Verificamos si la orden es un error en rojo
        ruleset=Ruleset.objects.get(name="analysis contract")
        rulesetImplementation=RulesetImplementation(ruleset)
        rulesetImplementation.executeRuleset(event)

        log.info('End: clasifyContract')




class AnalysisContractCPM:

    def getProcessInfo(contract):
        log.info('Start: getProcessInfo')
        processInfo={}
        query_processes="""select pi.objid, pi.start_time, pi.end_time, pi.status, pi.focus_lowid, pi.proc_inst2process, pc.ID, pc.version, pi.exec_tag as process_user
                               from  sa.table_proc_inst pi , sa.table_process pc 
                               where  pi.focus_lowid = %s  
                               and pi.proc_inst2process = pc.objid """  % (contract.objid)


        processes=smart_query.my_custom_sql('smart_gg', query_processes)
        processInfo['num_processes']=len(processes)
        processInfo['num_processes_completed']=len(list(filter(lambda x: x['status'] == 'COMPLETE', processes)))
        if (processInfo['num_processes']!=0):
            log.info('Analyizing contract:'+contract.s_id+' num_processes:'+str(processInfo['num_processes'])+ ' num_processes_completed:'+str(processInfo['num_processes_completed']))
            if (processInfo['num_processes'] != processInfo['num_processes_completed']):
                pendingProcesses=[]
                
                for processInstance in list(filter(lambda x: x['status'] != 'COMPLETE', processes)):
                    log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id']))
                    processInfo['process_id']=processInstance['id']
                    processInfo['process_user']=processInstance['process_user']
                    query_subprocesses= """select info.* 
                                            from 
                                                    ( select ri.objid, ri.start_time,ri.end_time,ri.status,ri.focus_lowid,
                                                    case 
                                                        when fg.id like '%s' then fg.id
                                                        when fg.id like '%s' then fg.id
                                                        else ri.id
                                                    end as taskid,
                                                    ri.id,
                                                    ri.rqst_inst2proc_inst, ri.rqst_inst2proc_inst as proc_inst, 
                                                    CASE WHEN to_char(ri.end_time,'yyyymmdd')='17530101' THEN SYSDATE+1000 ELSE  ri.end_time END AS FECHA_FIN
                                                    from sa.table_rqst_inst ri
                                                        left join (sa.table_group_inst gi) on (gi.objid = ri.rqst_inst2group_inst)
                                                        left join (sa.table_function fu) on ( fu.objid = gi.group2function)
                                                        left join (sa.table_func_group fg) on (fg.objid = fu.belongs2func_group)
                                                    where rqst_inst2proc_inst = %s
                                                    order by FECHA_FIN desc, ri.start_time desc, ri.objid desc
                                                    ) info
                                                where rownum=1""" % ('%[C]%', '%Cancelacion%', processInstance['objid'])
                    

                    tasks=smart_query.my_custom_sql('smart_gg', query_subprocesses)
                    if (len(tasks)==0):  
                        log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id'])+ ' Task:None')                          
                        processInfo['task']=None
                    else:
                        task=tasks[0]
                        log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id'])+ ' Task:'+str(task['taskid']))                          
                        task.pop('fecha_fin')
                        if (task['status']=='ERROR'):
                            log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id'])+ ' Task:'+str(task['taskid'])+ ' Analysis:Error' )                          
                            processInfo['task']=task
                            processInfo['task_details']=AnalysisContractCPM.getServiceRequest(task['id'])
                            break
                        elif (task['status']=='WAITING'):
                            (isBlockingTask, task_details)=AnalysisContractCPM.verifyWaiting(contract.objid, processInstance, task, processes)
                            log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id'])+ ' Task:'+str(task['taskid'])+ ' Analysis:'+ isBlockingTask)                          
                            if (isBlockingTask=='BLOCKING'):
                                    processInfo['task']=task
                                    processInfo['task_details']=task_details
                                    processInfo['task_details'].update(AnalysisContractCPM.getServiceRequest(task['id']))
                                    break
                            elif (isBlockingTask=='POTENTIAL'):     
                                    processInfo['task']=task
                                    processInfo['task_details']=task_details
                                    processInfo['task_details'].update(AnalysisContractCPM.getServiceRequest(task['id']))
                            elif ( isBlockingTask=='NOBLOCKING' and not 'task' in processInfo):
                                    processInfo['task']=task
                                    processInfo['task_details']=task_details
                                    processInfo['task_details'].update(AnalysisContractCPM.getServiceRequest(task['id']))
                        elif (task['status']=='COMPLETE' or task['status']=='CANCELLED'):
                            log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['id'])+ ' Task:'+str(task['taskid'])+ ' Analysis: Process not completed and tasks complete' )
                            processInfo['task']=task
                            processInfo['task_details']=AnalysisContractCPM.getServiceRequest(task['id'])
                            break
                

                if ('task' in processInfo and processInfo['task']):
                    if task['status']=='WAITING':
                            validation=AnalysisProcessInstanceComb.getValidations(contract.objid, task['start_time'] )
                            if (validation):
                                processInfo['task_details'].update({'validation':validation})
                    elif task['status']=='ERROR':        
                            error=AnalysisOnolog.getOnologError(contract.objid, task['rqst_inst2proc_inst'], task['start_time'], False)
                            if (error):
                                processInfo['task_details'].update({'error':error})
        
        log.info('End: getProcessInfo')
        return processInfo
        

    #   inputs:
    #       contractObjid: Objid de contract
    #       processInstance: Objeto de la instancia del proceso que se esta analizando     
    #       task: Objeto de la tarea que se esta analizando
    #   output:
    #       return BLOCKING si la tarea tiene un estado Waiting que es bloqueante
    #              POTENTIAL si la tarea tiene un estado Waiting que es potencialmente bloqueante
    #              NOBLOCKING si la tarea tiene un estado Waiting que es NO bloqueante
    #  
    def verifyWaiting(contractObjid, processInstance, task, processes):
        log.info('Start: verifyWaiting')
        if task['id']=='Fin Cierre Orden':
            query_cierre_orden= """ select  case
                                                when    x_fecha_cancelacion is not null 
                                                    and to_char(x_fecha_cancelacion,'yyyymmdd')<>'17530101' then  'CANCELLING'
                                                else   'INPROGRESS'
                                            end AS status,
                                            NVL(PC.X_CMB_CIERRE_ORDEN, 0) as x_cmb_cierre_orden,
                                            NVL(X_CMB_CANC_CIERRE_ORDEN, 0) as  x_cmb_canc_cierre_orden           
                                     from   SA.TABLE_X_PM_CONTRACT PC
                                    where   PC.X_PM2CONTRACT = %s""" % (contractObjid)
            query_cierre_orden_output=smart_query.my_custom_sql('smart_gg', query_cierre_orden)
            if (len(query_cierre_orden_output)>0):  
                if (query_cierre_orden_output[0]['status']=='INPROGRESS'):
                    esperaCierre=query_cierre_orden_output[0]['x_cmb_cierre_orden']
                    statusWaiting='BLOCKING' if esperaCierre==1 else 'NOBLOCKING'
                    return (statusWaiting, {'message':'table_x_pm_contract.x_cmb_cierre_orden = 1', 'value':'table_x_pm_contract.x_cmb_cierre_orden : '+ str(esperaCierre)})
                else:
                    esperaCierre=query_cierre_orden_output[0]['x_cmb_canc_cierre_orden']
                    statusWaiting='BLOCKING' if esperaCierre==1 else 'NOBLOCKING'
                    return (statusWaiting, {'message':'table_x_pm_contract.x_cmb_canc_cierre_orden = 1', 'value':'table_x_pm_contract.x_cmb_canc_cierre_orden : '+ str(esperaCierre)})

            else:
                return ('NOBLOCKING', {'message':'table_x_pm_contract.x_cmb_cierre_orden = 1', 'value':'table_x_pm_contract.x_cmb_cierre_orden : null' })    
        elif task['id']=='Inicio Facturacion':
            query_ini_facturacion= """ select  NVL(PC.x_cmb_inic_facturacion, 0) as x_cmb_inic_facturacion
                                       from   SA.TABLE_X_PM_CONTRACT PC
                                       where   PC.X_PM2CONTRACT = %s""" % (contractObjid)
            query_ini_facturacion_output=smart_query.my_custom_sql('smart_gg', query_ini_facturacion)
            if (len(query_ini_facturacion_output)>0):  
                ini_facturacion=query_ini_facturacion_output[0]['x_cmb_inic_facturacion']
                statusWaiting='BLOCKING' if ini_facturacion==1 else 'NOBLOCKING'
                return (statusWaiting, {'message':'table_x_pm_contract.x_cmb_inic_facturacion = 1', 'value':'table_x_pm_contract.x_cmb_inic_facturacion : '+ str(ini_facturacion)})
            else:
                return ('NOBLOCKING', {'message':'table_x_pm_contract.x_cmb_inic_facturacion = 1', 'value':'table_x_pm_contract.x_cmb_inic_facturacion :null' })    

#X_CMB_CANC_CIERRE_ORDEN       
        elif task['id']=='Fin Provision':   
             return ('NOBLOCKING',{})    
        else:
            #Verificanos dependencias
            if (not AnalysisContractCPM.verifyDependences(contractObjid, processInstance, task, processes)):
                return ('BLOCKING', {'message':'Error Task waiting but dependent tasks are completed', 'value':'Error Task waiting but dependent tasks are completed'})

            #Verificamos combinados  
            if (not AnalysisContractCPM.verifyCombine(contractObjid, processInstance, task, processes)):  
                return ('BLOCKING', {'message':'Error Task waiting but combined tasks are completed', 'value':'Error Task waiting but combined tasks are completed'})

            (isBlockingTask, task_details)=AnalysisContractCPM.verifyWaitingCondition(task['objid'], processInstance['objid'], contractObjid)
            if (isBlockingTask=='BLOCKING'):
                return (isBlockingTask, task_details)
            else:
                return ('POTENTIAL',{}) 


    

    #   inputs:
    #       taskObjid: Objid de la tarea que se esta analizando
    #       processInstance: Objid de la instancia del proceso que se esta analizando
    #       contract: Objid de la tarea que se esta analizando.
    #   output:
    #       return "details" que es un diccionario con toda la información recopilada de la tarea
    #       
    def verifyWaitingCondition(taskObjid, processInstance, contract):
        log.info('Start: verifyWaitingCondition')
        details={}
        condition=""
        query_condition =    """select giLevel, fg.COND_PATH, fg.ITER_PATH, fg.ID, f.VALUE
                                from (select level as giLevel, gi.*
                                        from sa.table_group_inst gi
                                        start with gi.objid = (select ri.rqst_inst2group_inst
                                                                from sa.table_rqst_inst ri
                                                                where ri.objid = %s)
                                        connect by prior gi.child2group_inst = gi.objid) group_inst
                                inner join(sa.table_func_group fg) on (fg.objid = group_inst.group2func_group)
                                left join(sa.table_function f)     on (f.belongs2func_group=fg.objid)
                                order by giLevel ASC""" % (taskObjid)
        tasks=smart_query.my_custom_sql('smart_gg', query_condition)
        for task in tasks:
            if  (('cond_path' in task) and (task['cond_path'])):
                condition='if '+ task['cond_path'].replace('$GroupInst:all_group_inst2proc_inst:','')

                if (('value' in task) and (task['value']) and (task['value'].strip()!='')):
                    condition += ' == ' + task['value']
                break
            elif  (('iter_path' in task) and (task['iter_path'])):
                condition='while ' + task['iter_path'].replace('$GroupInst:all_group_inst2proc_inst:','')
                break
        

        if (condition):
            details['message']=condition
            details['value']=None
            if (condition.strip()!=''):  
                try:      
                   
                    if (('contract2x_pm_corp' in condition) or ('proc_inst2x_pm_corp' in condition)):
                        fields=condition.split(':')
                        if (len(fields)>1):
                            field=fields[1]
                            field_aux=field.split(' ')
                            field= field_aux[0] if (len(field_aux)>1) else field
                            query_details= """ select %s
                                            from sa.table_x_pm_corp 
                                            where x_pm_corp2proc_inst=%s """ % (field, processInstance)
                            query_details_output=smart_query.my_custom_sql('smart_gg', query_details)
                            if (len(query_details_output)>0):  
                                #details['value']=query_details_output[0][field] 
                                details['value']='table_x_pm_corp.'+ field + ' : ' + str(query_details_output[0][field])
                    elif ('contract2x_pm' in condition):
                        fields=condition.split(':')
                        if (len(fields)>1):
                            field=fields[1]
                            field_aux=field.split(' ')
                            field= field_aux[0] if (len(field_aux)>1) else field
                            query_details= """ select %s
                                            from sa.table_x_pm_contract 
                                            where x_pm2contract=%s """ % (field, contract)
                            query_details_output=smart_query.my_custom_sql('smart_gg', query_details)
                            if (len(query_details_output)>0):  
                                #details['value']=query_details_output[0][field]
                                details['value']='table_x_pm_contract.'+field+' : ' + str(query_details_output[0][field])
                except:
                    pass
            
            log.info('End: verifyWaitingCondition')
            return ('BLOCKING', details)
        else:
            if ('[M]' in tasks[-1]['id']):
                log.info('End: verifyWaitingCondition')
                return ('BLOCKING', {'message':'Manual Task', 'value':'Manual Task'}) 
            log.info('End: verifyWaitingCondition')
            return ('NOBLOCKING',{})


    #   inputs:
    #       contractObjid: Objid de contract
    #       processInstance: Objeto de la instancia del proceso que se esta analizando
    #       task: Objeto de la tarea que se esta analizando.
    #   output:
    #       return True si la tarea no tiene dependencias o todavia no tiene que ejecutarse
    #       False si la tarea tiene dependencias y ya se han completado todas ellas
    #       
    def verifyDependences(contractObjid, processInstance, task, processes):
        log.info('Start: verifyDependences')

        list_processes=list(map(lambda x:x['id'],processes))
        list_processes_str="'"+"','".join(list_processes)+"'"

        #Verificanos dependencias
        query_def_dependencias="""select distinct x_proceso_hito, x_tarea_hito
                                    from sa.table_x_confproc_corp
                                    where x_proceso_dependiente = '%s'
                                    and x_tarea_dependiente = '%s' 
                                    and x_proceso_dependiente in (%s) """ %(processInstance['id'],task['id'],list_processes_str) 
        query_def_dependencias_output=smart_query.my_custom_sql('smart_replica', query_def_dependencias)
        if (len(query_def_dependencias_output)>0):
            list_task_processes=list(map(lambda x:"('"+x['x_tarea_hito']+"','"+x['x_proceso_hito']+"')",query_def_dependencias_output))
            list_task_processes_str=",".join(list_task_processes)

            query_verify_dependencias= """  select count(*) as numtask
                                            from sa.table_proc_inst pi, sa.table_process pc, sa.table_rqst_inst ri
                                            where pi.focus_lowid = %s
                                            and pi.proc_inst2process = pc.objid
                                            and pi.objid = ri.rqst_inst2proc_inst
                                            and (ri.id, pc.iD) in (%s)
                                            and ri.STATUS = 'COMPLETE'
                                        """ %(contractObjid,list_task_processes_str) 
            query_verify_dependencias_output=smart_query.my_custom_sql('smart_gg', query_verify_dependencias)
            data_dependencias=query_verify_dependencias_output[0]

            log.info('End: verifyDependences')    
            return len(query_def_dependencias_output)!=data_dependencias['numtask']
        
        log.info('End: verifyDependences') 
        return True


    #   inputs:
    #       contractObjid: Objid de contract
    #       processInstance: Objeto de la instancia del proceso que se esta analizando
    #       task: Objeto de la tarea que se esta analizando.
    #   output:   
    #       return True si la tarea no tiene dependencias o todavia no tiene que ejecutarse
    #       False si la tarea tiene dependencias y ya se han completado todas ellas    
    #         
    def verifyCombine(contractObjid, processInstance, task, processes):
        log.info('Start: verifyCombine')

        list_processes=list(map(lambda x:"('"+x['id']+"',"+str(x['version'])+")",processes))
        list_processes_str=",".join(list_processes)

        #Verificanos dependencias
        query_def_combine="""  select distinct X_PROCESS_ID, X_ACTION_ID, X_VERSION
                               from SA.TABLE_X_DEF_COMBINADOS C
                               where X_ACTION_ID = '%s' 
                               and X_PROCESS_ID <> '%s'
                               and (X_PROCESS_ID, X_VERSION) in (%s) """ %(task['id'],processInstance['id'], list_processes_str) 

        query_def_combine_output=smart_query.my_custom_sql('smart_gg', query_def_combine)
        if (len(query_def_combine_output)>0):  

            list_task_processes=list(map(lambda x:"('"+x['x_action_id']+"','"+x['x_process_id']+"',"+str(x['x_version'])+")",query_def_combine_output))
            list_task_processes_str=",".join(list_task_processes)

            query_verify_combine= """  select count(*) as numtask
                                        from sa.table_proc_inst pi, sa.table_process pc, sa.table_rqst_inst ri
                                        where pi.focus_lowid = %s
                                        and pi.proc_inst2process = pc.objid
                                        and pi.objid = ri.rqst_inst2proc_inst
                                        and (ri.id, pc.iD, pc.VERSION) in (%s)
                                        and ri.STATUS = 'COMPLETE'
                                        """ %(contractObjid,list_task_processes_str) 
            query_verify_combine_output=smart_query.my_custom_sql('smart_gg', query_verify_combine)
            data_combine=query_verify_combine_output[0]
            log.info('End: verifyCombine')
            return len(query_def_combine_output)!=data_combine['numtask']

        log.info('End: verifyCombine')
        return True

    #   inputs:
    #       contract: Objid de contract
    #   output:
    #       return el registro con el service request y el pl al que se invoca en la tarea
    #
    def getServiceRequest(taskId):
        log.info('Start: getServiceRequest')

        output={}
        query_sr_pl= """ select NVL(d.description, '') as PL, NVL(rq.svc_name, '') as SR
                                from SA.TABLE_SVC_RQST rq, sa.table_rqst_def d
                                where rq.id = '%s'
                                and d.svc_name = rq.svc_name
                                and rownum = 1""" % (taskId)

        query_sr_pl_output=smart_query.my_custom_sql('smart_replica', query_sr_pl)
        if (len(query_sr_pl_output)>0):  
            pl=query_sr_pl_output[0]['pl']
            sr=query_sr_pl_output[0]['sr']
            if (len(sr)>0):
                output['service_request']=sr
            if (len(pl)>0):
                output['procedure']=pl

        log.info('End: getServiceRequest')

        return output

class AnalysisContractAPM:        
    
    def mapStepInstanceStatus(status, list_of_map):
        log.info('Start: mapStepInstanceStatus')
        mapInfo = next((statusMapped for statusMapped in list_of_map if statusMapped['value'] == status), None)
        if (mapInfo):
            log.info('End: mapStepInstanceStatus')
            return mapInfo['status']
        else:
            log.info('End: mapStepInstanceStatus')
            return 'OTHER'    

    ############################################################################################
    #   inputs:
    #       contractObjid: Objid de contract
    #       statusProcessInstance: Estado del proceso
    #       task: Objeto de la tarea que se esta analizando
    #   output:
    #       return BLOCKING si la tarea tiene un estado Waiting que es bloqueante
    #              POTENTIAL si la tarea tiene un estado Waiting que es potencialmente bloqueante
    #              NOBLOCKING si la tarea tiene un estado Waiting que es NO bloqueante
    #  
    ############################################################################################
    def verifyWaitingAPM(contractObjid, statusProcessInstance, task):
        log.info('Start: verifyWaiting')
        if task['id']=='Fin Cierre Orden':
            query_cierre_orden= """ select  NVL(PC.X_CMB_CIERRE_ORDEN, 0) as x_cmb_cierre_orden,
                                            NVL(X_CMB_CANC_CIERRE_ORDEN, 0) as  x_cmb_canc_cierre_orden           
                                     from   SA.TABLE_X_PM_CONTRACT PC
                                    where   PC.X_PM2CONTRACT = %s""" % (contractObjid)
    
            query_cierre_orden_output=smart_query.my_custom_sql('smart_gg', query_cierre_orden)
            if (len(query_cierre_orden_output)>0):  
                if (statusProcessInstance!="cancelling"):
                    esperaCierre=query_cierre_orden_output[0]['x_cmb_cierre_orden']
                    statusWaiting='BLOCKING' if esperaCierre==1 else 'NOBLOCKING'
                    return statusWaiting
                else:
                    esperaCierre=query_cierre_orden_output[0]['x_cmb_canc_cierre_orden']
                    statusWaiting='BLOCKING' if esperaCierre==1 else 'NOBLOCKING'
                    return statusWaiting

            else:
                return 'NOBLOCKING'

        elif task['id']=='Inicio Facturacion':
            query_ini_facturacion= """ select  NVL(PC.x_cmb_inic_facturacion, 0) as x_cmb_inic_facturacion
                                       from   SA.TABLE_X_PM_CONTRACT PC
                                       where   PC.X_PM2CONTRACT = %s""" % (contractObjid)
            query_ini_facturacion_output=smart_query.my_custom_sql('smart_gg', query_ini_facturacion)
            if (len(query_ini_facturacion_output)>0):  
                ini_facturacion=query_ini_facturacion_output[0]['x_cmb_inic_facturacion']
                statusWaiting='BLOCKING' if ini_facturacion==1 else 'NOBLOCKING'
                return statusWaiting
            else:
                return 'NOBLOCKING'
    
        elif task['id']=='Fin Provision':   
            return 'NOBLOCKING'
        else:
            return 'POTENTIAL'

    
    def getProcessInfo(contract):
        log.info('Start: getProcessInfo')

        apmProcessInfo={}
        #take the root states of APM process
        root_status_process_apm_param=Appparameter.objects.get(name__iexact='Root status process APM')
        root_status_process_apm=root_status_process_apm_param.getParamaterDataValue()
        #take the root states of APM process
        status_process_apm_param=Appparameter.objects.get(name__iexact='Status process APM')
        status_process_apm=status_process_apm_param.getParamaterDataValue()
        #take the step states of APM process
        status_step_apm_param=Appparameter.objects.get(name__iexact='Step status APM')
        status_step_apm_param=status_step_apm_param.getParamaterDataValue()


        query_apm_processes=""" select name, status, root_status, objid, x_alt_objid, creation_time, assignee as process_user
                                from sa.table_bpm_proc_inst
                                where focus_objid = %s
                                and parent2proc_inst is null
                                order by creation_time desc """  % (contract.objid)


        apm_processes=smart_query.my_custom_sql('smart_gg', query_apm_processes)
        apmProcessInfo['num_processes']=len(apm_processes)
        numCompleted=0
        #Obtenemos el número de procesos ejecutados.
        for item in apm_processes:
            if (AnalysisContractAPM.isAPMProcessCompleted(item)):
                numCompleted+=1

        apmProcessInfo['num_processes_completed']=numCompleted

        #Una vez que hemos revisado los processos 
        log.info('Analyizing contract APM:'+contract.s_id+' num_processes:'+str(apmProcessInfo['num_processes'])+ ' num_processes_completed:'+str(apmProcessInfo['num_processes_completed']))
        if (apmProcessInfo['num_processes'] != apmProcessInfo['num_processes_completed']):
            #Como no tiene todos los procesos completados, recorremos las tareas para ver cual es el problema
            #for processInstance in list(filter(lambda x: (x['status'] != 10 and x['root_status'] != 0), apm_processes)):
            for apmProcess in apm_processes:
                if (not AnalysisContractAPM.isAPMProcessCompleted(apmProcess)):            
                    processInstance=apmProcess
                    log.info('Analyizing contract:'+contract.s_id+' Process:'+processInstance['name'])
                    apmProcessInfo['process_id']=processInstance['name']
                    apmProcessInfo['process_user']=processInstance['process_user']
                    query_subprocesses= """ select info.* 
                                            from
                                                (select objid as apm_objid, %s as focus_lowid, name as id, start_time, status_change_time, status, parent2proc_inst, root2proc_inst, step2step, x_alt_objid as objid, %s as proc_inst, curr_fault2fault_info
                                                from sa.table_bpm_step_inst
                                                where root2proc_inst='%s' 
                                                and x_alt_objid is not null
                                                order by x_alt_objid desc
                                                ) info
                                            where rownum<=2 """ % (contract.objid, processInstance['x_alt_objid'], processInstance['objid'])
                    
                    tasks=smart_query.my_custom_sql('smart_gg', query_subprocesses)
                    #Lo comneto porque no estoy seguro map(lambda x : x*2, tasks) 
                    if (len(tasks)==0):  
                        log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['name'])+ ' Task:None')                                                                          
                    else:
                        task=tasks[0]
                        task['taskid']=task['id']
                        log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['name'])+ ' Task:'+str(task['id']))

                        task['status']=AnalysisContractAPM.mapStepInstanceStatus(task['status'], status_step_apm_param)
                        if (task['status'] != 'WAITING'):
                            break
                        else:
                            #Analizamos el tipo de WAITING
                            statusProcessInstance=AnalysisContractAPM.mapStepInstanceStatus(processInstance['root_status'], root_status_process_apm)
                            isBlockingTask=AnalysisContractAPM.verifyWaitingAPM(contract.objid, statusProcessInstance, task)

                            log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['name'])+ ' Task:'+str(task['id'])+ ' Analysis:'+ isBlockingTask)                          
                            if (isBlockingTask=='BLOCKING'):
                                break
                            elif (isBlockingTask=='POTENTIAL'):     
                                pass
            
            if (not tasks):
                apmProcessInfo['task']=None
            elif (len(tasks)==0):
                apmProcessInfo['task']=None
            else:
                task=tasks[0]
                log.info('Analyizing Details contract:'+contract.s_id+' Process:'+str(processInstance['name'])+ ' Task:'+str(task['id']))

                #El estado que tiene una tarea completada es 65 (finished)                    
                if (task['status']!='COMPLETE'):
                    log.info('Analyizing contract:'+contract.s_id+' Process:'+str(processInstance['name'])+ ' Task:'+str(task['id'])+ ' Analysis:Error' )                          
                    apmProcessInfo['task']=task
                    apmProcessInfo['task_details']=AnalysisContractAPM.getServiceRequest(task['step2step'])

                    faultInfo=AnalysisContractAPM.getFault(task['curr_fault2fault_info'], status_step_apm_param)

                    error=None
                    validation=None
                    if (faultInfo):
                        error=AnalysisOnolog.getOnologError(contract.objid, processInstance['x_alt_objid'], faultInfo['fault_time'], True) 
                        validation=AnalysisProcessInstanceComb.getValidations(contract.objid, faultInfo['fault_time'])                  
                    else:                        
                        if (tasks[1]):
                            
                            #error=AnalysisOnolog.getOnologErrorRangeDates(contract.objid, processInstance['x_alt_objid'], tasks[1]['start_time'], task['start_time']+datetime.timedelta(seconds=10))
                            startDate=tasks[1]['start_time'] if tasks[1]['start_time'] else tasks[1]['status_change_time']                             
                            endDate=task['start_time'] if task['start_time'] else task['status_change_time'] 
                            validation=AnalysisProcessInstanceComb.getValidations(contract.objid, startDate)   
                            error=AnalysisOnolog.getOnologErrorRangeDates(contract.objid, processInstance['x_alt_objid'], startDate, endDate + datetime.timedelta(seconds=10))
                        else:
                            startDate=task['start_time'] if task['start_time'] else task['status_change_time'] 
                            endDate=task['start_time'] if task['start_time'] else task['status_change_time'] 
                            validation=AnalysisProcessInstanceComb.getValidations(contract.objid, startDate)           
                            error=AnalysisOnolog.getOnologErrorRangeDates(contract.objid, processInstance['x_alt_objid'], startDate-datetime.timedelta(seconds=1), endDate+datetime.timedelta(seconds=10))                          

                    if (error):
                        apmProcessInfo['task_details']['error']=error     

                    if (validation):    
                        apmProcessInfo['task_details']['validation']=validation 
                    
        log.info('End: getProcessInfo')

        return  apmProcessInfo

    #   inputs:
    #       contract: Objid del paso de la tarea
    #   output:
    #       return el registro con el valor del Service Request al que invoca la tarea
    #
    def getServiceRequest(taskStepObjid):
        log.info('Start: getServiceRequest')

        output={}
        query_sr= """ select NVL(step.svc_name, '') as sr
                      from sa.table_bpm_step step
                      where step.objid = '%s'
                      and rownum = 1""" % (taskStepObjid)

        query_sr_output=smart_query.my_custom_sql('smart_gg', query_sr)
        if (len(query_sr_output)>0):  
            query_sr_def= """ select  NVL(def.description,'') as description, NVL(def.svc_name,'') as svc_name
                         from sa.table_rqst_def def
                         where upper(def.svc_name||'.'||def.svc_name) = upper('%s')
                         and rownum=1 """ % (query_sr_output[0]['sr'])


            query_sr_def_output=smart_query.my_custom_sql('smart_replica', query_sr_def)

            if (len(query_sr_def_output)>0): 

                output['procedure']=query_sr_def_output[0]['description'].strip() if (query_sr_def_output[0]['description']) else ''

                if (query_sr_def_output[0]['svc_name'] and query_sr_def_output[0]['svc_name'].strip()!=''):
                    output['service_request']=query_sr_def_output[0]['svc_name'].strip()
                else:
                    output['service_request'] =query_sr_output[0]['sr'].strip() if (query_sr_output[0]['sr']) else ''  
            else:
                output['service_request'] =query_sr_output[0]['sr'].strip() if (query_sr_output[0]['sr']) else ''   


        log.info('End: getServiceRequest')

        return output

    
    #   inputs:
    #       objid: Objid del fault
    #   output:
    #       return el registro con el valor del fault
    #
    def getFault(objid, list_of_map):
        log.info('Start: getFault')

        if (objid):
            query_fault= """ select *
                        from sa.table_bpm_fault_info faultInfo
                        where objid = '%s' """ % (objid)

            query_fault_output=smart_query.my_custom_sql('smart_gg', query_fault)
            if (len(query_fault_output)>0): 
                output=query_fault_output[0]
            else:
                output=None   
        else:
            output=None         
            
        log.info('End: getFault')

        return output


    # ####################################################################
    # Metodo para verificar si un proceso esta completado
    # 
    # input processInfo     informacion del proceso
    #
    # output boolean True si el proceso esta completado
    #
    # ####################################################################
    def isAPMProcessCompleted(processInfo):
        output=False
        if ((processInfo['root_status']==0 or processInfo['root_status']==10) and processInfo['status']==10):
            return True
        elif (processInfo['root_status']==15):
            return True
        return False        

