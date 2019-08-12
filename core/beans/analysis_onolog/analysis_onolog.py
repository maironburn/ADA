from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
import traceback
import json
import datetime
from json_tricks import dumps
from core.vodafone.smart import smart_query

log = logging.getLogger(__name__)
class AnalysisOnolog:
    #   inputs:
    #       contract: Objid de contract
    #       processInstance: Objeto de la instancia del proceso que se esta analizando
    #       searchDate: Fecha a partir de la cual buscar
    #       exactDate: Si es True se busca el log en la fecha exacta
    #                  Si es False se busca a partir de la fecha.
    #   output:
    #       return el registro de error recuperado de la tabla onolog, en caso contrario devuelve nulo
    #
    def getOnologError(contractObjid, processInstance, searchDate, exactDate):
        log.info('Start: getOnologError')
        #Prueba Andres
        if (searchDate.__class__.__name__ == 'datetime'):
            strSearchDate=searchDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            strSearchDate=searchDate
        #prueba Andres
        output={}

        query_base_get_logs="""  select /*+ INDEX (logT NBS_ONOLOG2CONTRACT) */  rownum, logT.package, logT.procedure_name, logT.action,logT.sqlcode, logT.errmsg, logT.log_step, logT.comments, logT.process_instance, logT.time 
                            from  sa.onolog logT
                            where logT.contract= %s"""  % (contractObjid) 
        if (exactDate):
            query_base_get_logs += " and  logT.time>=TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS') - INTERVAL '10' SECOND " % (strSearchDate)
            query_base_get_logs += " and  logT.time<=TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS') + INTERVAL '10' SECOND " % (strSearchDate)
        else:                         
            query_base_get_logs += " and logT.time>=TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS') " %(strSearchDate)

        if (processInstance and processInstance != 0 ):
              query_base_get_logs +=  " and   (logT.process_instance IS NULL OR logT.process_instance= %s) " %(processInstance)

        #query_get_logs=  query_base_get_logs +  " and (logT.sqlcode != 0) and (logT.sqlcode is not null) "
        query_get_logs=  query_base_get_logs +  " order by logT.time desc "             

        query_get_logs_output=smart_query.my_custom_sql('smart_replica', query_get_logs)
        if (len(query_get_logs_output)>0):  
            record=query_get_logs_output[0]

            logs_to_analyze=list(filter(lambda x: (x['time'] >= (record['time'] - datetime.timedelta(seconds=10))  and x['rownum']!=record['rownum']), query_get_logs_output))
            
            tmp=AnalysisOnolog.analyzeOnologRecords(record,logs_to_analyze )
            if (tmp):
                tmp.pop('rownum')
                log.info('End: getOnologError')
                return tmp
            else:
                record.pop('rownum') 
                log.info('End: getOnologError')           
                return record

        else:
            log.info('End: getOnologError')
            return None


    #   inputs:
    #       contract: Objid de contract
    #       processInstance: Objeto de la instancia del proceso que se esta analizando
    #       searchDate: Fecha a partir de la cual buscar
    #       exactDate: Si es True se busca el log en la fecha exacta
    #                  Si es False se busca a partir de la fecha.
    #   output:
    #       return el registro de error recuperado de la tabla onolog, en caso contrario devuelve nulo
    #
    def getOnologErrorRangeDates(contractObjid, processInstance, startDate, endDate):
        log.info('Start: getOnologErrorRangeDates')

        if (startDate.__class__.__name__ == 'datetime'):
            strStartDate=startDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            strStartDate=startDate

        if (endDate.__class__.__name__ == 'datetime'):
            strEndDate=endDate.strftime('%Y-%m-%d %H:%M:%S')
        else:
            strEndDate=endDate  
                  
        output={}

        query_base_get_logs="""  select /*+ INDEX (logT NBS_ONOLOG2CONTRACT) */  rownum, logT.package, logT.procedure_name, logT.action,logT.sqlcode, logT.errmsg, logT.log_step, logT.comments, logT.process_instance, logT.time 
                                 from  sa.onolog logT
                                 where logT.contract= %s"""  % (contractObjid) 
        query_base_get_logs += " and  logT.time>=TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS') " % (strStartDate)
        query_base_get_logs += " and  logT.time<=TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS') " % (strEndDate)

        if (processInstance and processInstance != 0 ):
              query_base_get_logs +=  " and   (logT.process_instance IS NULL OR logT.process_instance= %s) " %(processInstance)

        #query_get_logs=  query_base_get_logs +  " and (logT.sqlcode != 0) and (logT.sqlcode is not null) "
        query_get_logs=  query_base_get_logs +  " order by logT.time desc "             

        query_get_logs_output=smart_query.my_custom_sql('smart_replica', query_get_logs)
        if (len(query_get_logs_output)>0):  
            record=query_get_logs_output[0]

            logs_to_analyze=list(filter(lambda x: (x['time'] >= (record['time'] - datetime.timedelta(seconds=10))  and x['rownum']!=record['rownum']), query_get_logs_output))
            
            tmp=AnalysisOnolog.analyzeOnologRecords(record,logs_to_analyze )
            if (tmp):
                tmp.pop('rownum')
                log.info('End: getOnologErrorRangeDates')
                return tmp
            else:
                record.pop('rownum')
                log.info('End: getOnologErrorRangeDates')
                return record

        else:
            log.info('End: getOnologErrorRangeDates')
            return None        

    #   inputs:
    #       record: registro base tomado como referencia.
    #       list_of_records: Lista de registros a analizar
    #   output:
    #       return el registro del error.
    #
    def analyzeOnologRecords(record, list_of_records):
        log.info('Start: analyzeOnologRecords')
        for item in list_of_records:
            if ((record['comments'])) and (item['procedure_name'].upper() in record['comments'].upper()):
                logs_to_analyze=list(filter(lambda x:  x['rownum']!=item['rownum'], list_of_records))
                tmp=AnalysisOnolog.analyzeOnologRecords(item,logs_to_analyze )
                if (tmp):
                    return tmp
                else:
                    return item
            elif ((not record['comments']) or (record['comments'].strip()=='')):
                logs_to_analyze=list(filter(lambda x:  x['rownum']!=item['rownum'], list_of_records))
                tmp=AnalysisOnolog.analyzeOnologRecords(item,logs_to_analyze )
                if (tmp):
                    return tmp
                else:
                    return item

        log.info('End: analyzeOnologRecords')
        return None
