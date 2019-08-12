from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
import traceback
import json
import datetime
from json_tricks import dumps
from core.vodafone.smart import smart_query

log = logging.getLogger(__name__)

class AnalysisProcessInstanceComb:
    
    
    #   inputs:
    #       contractObjid: Objid de contract
    #       searchDate: Fecha a partir de la cual buscar
    #   output:
    #       return una cadena con las validaciones localizadas
    #
    def getValidations(contractObjid, searchDate):
        log.info('Start: getValidations')
        strSearchDate=searchDate.strftime('%Y-%m-%d %H:%M:%S')
        query_get_logs="""select *
                          from 
                          (
                            select detalle, entrada 
                            from sa.nbspm_processinstancescomb
                            where contract = %s
                            and entrada >= TO_DATE('%s', 'YYYY-MM-DD HH24:MI:SS')
                            order by entrada desc
                          )
                         where rownum=1""" %(contractObjid, strSearchDate)

        query_get_logs_output=smart_query.my_custom_sql('smart_gg', query_get_logs)
        if (len(query_get_logs_output)>0):
            log.info('End: getValidations')
            return query_get_logs_output[0]
        else:
            log.info('End: getValidations')
            return None