from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from core.vodafone.smart.contract.models import Contract
from core.vodafone.smart.site.models import Site
from datetime import datetime
from core.vodafone.smart import smart_query

log = logging.getLogger(__name__)

class AnalysisLogs:

    def analyze(parameters) :

        log.info('Start: analyze')

        output=[]
        inputLogin=None
        inputOTHER=None

        if (not parameters):
            raise ApiException("Invalid parameters.")

        if (not "inputDate" in parameters or parameters["inputGAP"].strip()==""):
            inputDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        else:
            try:
                inputDate=datetime.strptime(parameters["inputDate"],'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                raise ApiException("Invalid parameters. inputDate format must be yyyy-mm-dd Hh24:MI:SS")

        if (not "inputGAP" in parameters or parameters["inputGAP"].strip()==""):
            inputGap=10
        else:
            try:
                inputGap=int(parameters["inputGAP"])
            except Exception:
                raise ApiException("Invalid parameters. inputGap must be numeric value less than 180 minutes")
        
        if (inputGap > 180):
                    raise ApiException("Invalid parameters. inputGap must be numeric value less than 180 minutes")
        
        if (not "inputOT" in parameters or parameters["inputOT"].strip()=="") and (not "inputSite" in parameters or parameters["inputSite"].strip()==""):
            raise ApiException("Invalid parameters. inputOT or inputSite are mandatory")
        
        if ("inputOT" in parameters and parameters["inputOT"].strip()!=""):
                try:
                    contract=Contract.objects.get(s_id=parameters["inputOT"])
                except Contract.DoesNotExist: 
                    raise ApiException("Invalid parameters. %s Contract not found" % parameters["inputOT"])

        if ("inputSite" in parameters and parameters["inputSite"].strip()!=""):
                try:
                    site=Site.objects.get(site_id=parameters["inputSite"])
                except Site.DoesNotExist: 
                    raise ApiException("Invalid parameters. %s Site not found" % parameters["inputSite"])
        else:
            #Obtenemos el site de la contract
            query_site = """select s.site_id
                            from table_site s,
                                    table_contr_schedule cs,
                                    table_contract c
                            where c.s_id= '%s' 
                            and c.objid=cs.schedule2contract
                            and cs.ship_to2site=s.objid """ % (contract.s_id)

            querySite=smart_query.my_custom_sql('smart_gg', query_site)
            if (len(querySite)==0):
                raise ApiException("Invalid parameters. Site not found from contract %s" % contract.s_id)
            else:    
                try:
                    site=Site.objects.get(site_id=querySite[0]["site_id"])
                except  Site.DoesNotExist:   
                    raise ApiException("Invalid parameters. Site not found from contract %s" % contract.s_id)

        if ("inputLogin" in parameters and parameters["inputLogin"].strip()!=""):
            inputLogin=parameters["inputLogin"]
        if ("inputOTHER" in parameters and parameters["inputOTHER"].strip()!=""):
            inputOTHER=parameters["inputOTHER"]
        
        #Busqueda en SC_LOG
        strFilter="0=1"

        if (contract):
            strFilter=strFilter + " OR parameters like '%{0}%' ".format(contract.s_id)+ " OR parameters like '%{0}%' ".format(contract.objid)
        
        if (site):
            strFilter=strFilter + " OR parameters like '%{0}%' ".format(site.site_id)+ " OR parameters like '%{0}%' ".format(site.objid)

        if (inputLogin):
            strFilter=strFilter + " OR UPPER(parameters) like '%{0}%' ".format(inputLogin.upper())
        
        if (inputOTHER):
            strFilter=strFilter + " OR UPPER(parameters) like '%{0}%' ".format(inputOTHER.upper())
        
        strQuery="""SELECT  UPPER('table_x_sc_log') AS TABLENAME, PACKAGE AS  PACKAGE_NAME , '' AS   BATCHJOB,  '' AS  ACTION, PROCEDURE_FUNCTION AS PROCEDURE_NAME,  TIME, PARAMETERS  AS   PARAMETERS,   ''  AS SQL_CODE, '' AS  ERRMSG, '' AS   LOG_STEP , '' AS  COMMENTS,  '' AS  SEQ , '' AS   MENSAJE,  ''  AS CONTRACT_OBJID, '' AS   CONTRACT_ID  
                    FROM    table_x_sc_log
                    WHERE   time>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE  
                    AND     time<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE  """.format(inputDate, inputGap)
        
        strQuery=strQuery+ "AND ({0}) ".format(strFilter)

        query=smart_query.my_custom_sql('smart_replica', strQuery)
        output.extend(query)
        
        #busqueda en X_SC_ONOLOG
        strFilter="0=1"

        if (contract):
            strFilter=strFilter + " OR x_comments like '%{0}%' ".format(contract.s_id)+ " OR x_comments like '%{0}%' ".format(contract.objid)
            strFilter=strFilter + " OR x_contract like '%{0}%' ".format(contract.s_id)+ " OR x_contract like '%{0}%' ".format(contract.objid)
        
        if (site):
            strFilter=strFilter + " OR x_comments like '%{0}%' ".format(site.site_id)+ " OR x_comments like '%{0}%' ".format(site.objid)
            strFilter=strFilter + " OR x_id like '%{0}%' ".format(site.site_id)+ " OR x_id like '%{0}%' ".format(site.objid)

        if (inputLogin):
            strFilter=strFilter + " OR UPPER(x_comments) like '%{0}%' ".format(inputLogin.upper())
        
        if (inputOTHER):
            strFilter=strFilter + " OR UPPER(x_comments) like '%{0}%' ".format(inputOTHER.upper())
        
        strQuery="""SELECT UPPER('table_x_sc_onolog') AS TABLENAME, X_PACKAGE AS  PACKAGE_NAME , X_BATCHJOB AS   BATCHJOB, X_ACTION AS  ACTION, X_PROCEDURE_NAME  AS  PROCEDURE_NAME,  X_TIME AS TIME, '' AS   PARAMETERS,   to_char(X_SQLCODE)  AS SQL_CODE, X_ERRMSG AS  ERRMSG, X_LOG_STEP AS   LOG_STEP ,  X_COMMENTS AS  COMMENTS,  '' AS  SEQ , '' AS   MENSAJE,  to_char(X_CONTRACT)  AS CONTRACT_OBJID, '' AS   CONTRACT_ID  
                    FROM    table_x_sc_onolog
                    WHERE   x_time>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE 
                    AND     x_time<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE """.format(inputDate, inputGap)
        
        strQuery=strQuery+ "AND ({0}) ".format(strFilter)

        query=smart_query.my_custom_sql('smart_replica', strQuery)
        output.extend(query)

        #busqueda en ONOLOG
        strFilter="0=1"

        if (contract):
            strFilter=strFilter + " OR comments like '%{0}%' ".format(contract.s_id)+ " OR comments like '%{0}%' ".format(contract.objid)
            strFilter=strFilter + " OR contract like '%{0}%' ".format(contract.s_id)+ " OR contract like '%{0}%' ".format(contract.objid)
        
        if (site):
            strFilter=strFilter + " OR comments like '%{0}%' ".format(site.site_id)+ " OR comments like '%{0}%' ".format(site.objid)
            strFilter=strFilter + " OR id like '%{0}%' ".format(site.site_id)+ " OR id like '%{0}%' ".format(site.objid)

        if (inputLogin):
            strFilter=strFilter + " OR UPPER(comments) like '%{0}%' ".format(inputLogin.upper())
        
        if (inputOTHER):
            strFilter=strFilter + " OR UPPER(comments) like '%{0}%' ".format(inputOTHER.upper())
        
        strQuery="""SELECT UPPER('onolog') AS TABLENAME, PACKAGE AS  PACKAGE_NAME , BATCHJOB AS   BATCHJOB, ACTION AS  ACTION, PROCEDURE_NAME  AS    PROCEDURE_NAME,  TIME, '' AS   PARAMETERS,   to_char(SQLCODE)  AS SQL_CODE, ERRMSG AS  ERRMSG, LOG_STEP AS  LOG_STEP , COMMENTS AS  COMMENTS,  '' AS  SEQ , ''  AS   MENSAJE,  to_char(CONTRACT)  AS CONTRACT_OBJID, '' AS   CONTRACT_ID  
                    FROM    onolog
                    WHERE   time>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE 
                    AND     time<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE """.format(inputDate, inputGap)
        
        strQuery=strQuery+ "AND ({0}) ".format(strFilter)

        query=smart_query.my_custom_sql('smart_replica', strQuery)
        output.extend(query)


        #busqueda en TABLE_X_COC_RESTRICC_LOG
        strFilter="0=1"

        if (contract):
            strFilter=strFilter + " OR x_contract_objid='{0}' ".format(contract.objid)
        
        if (site):
            strFilter=strFilter + " OR x_site_objid='{0}' ".format(site.objid)
        
        strQuery="""SELECT UPPER('TABLE_X_COC_RESTRICC_LOG') AS TABLENAME, '' AS  PACKAGE_NAME , '' AS  BATCHJOB, '' AS ACTION, '' AS  PROCEDURE_NAME, X_LAST_UPDATE AS TIME, '' AS  PARAMETERS, ''  AS SQL_CODE, '' AS  ERRMSG, '' AS   LOG_STEP , '' AS  COMMENTS,  to_char(X_SEQ) AS  SEQ , X_MENSAJE AS   MENSAJE,  to_char(X_CONTRACT_OBJID)  AS CONTRACT_OBJID, '' AS   CONTRACT_ID  
                    FROM    TABLE_X_COC_RESTRICC_LOG
                    WHERE   x_last_update>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE  
                    AND     x_last_update<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE """.format(inputDate, inputGap)
        
        strQuery=strQuery+ "AND ({0}) ".format(strFilter)
        strQuery=strQuery+ "AND  x_mensaje <> 'OK' "

        query=smart_query.my_custom_sql('smart_replica', strQuery)
        output.extend(query)

        #busqueda en NBSPM_PROCESSINSTANCESCOMB
        #Solo se lanza si hay contract
        if (contract):
            strFilter=""
            strFilter=strFilter + " CONTRACT='{0}' ".format(contract.objid)
        
            strQuery="""SELECT UPPER('NBSPM_PROCESSINSTANCESCOMB') AS TABLENAME,  '' AS PACKAGE_NAME , '' AS  BATCHJOB, '' AS ACTION, ''  AS  PROCEDURE_NAME, ENTRADA AS TIME, '' AS  PARAMETERS, '' AS SQL_CODE, '' AS  ERRMSG, '' AS   LOG_STEP , '' AS  COMMENTS,  '' AS  SEQ , DETALLE AS   MENSAJE,  to_char(CONTRACT)  AS CONTRACT_OBJID, CONTRACT_ID AS  CONTRACT_ID  
                        FROM    NBSPM_PROCESSINSTANCESCOMB
                        WHERE   entrada>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE 
                        AND     entrada<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE  """.format(inputDate, inputGap)
            
            strQuery=strQuery+ "AND ({0}) ".format(strFilter)

            query=smart_query.my_custom_sql('smart_replica', strQuery)
            output.extend(query)


        #busqueda en TABLE_X_SC_TRAZAS_WS
        strFilter="0=1"

        if (contract):
            strFilter=strFilter + " OR x_traza like '%{0}%' ".format(contract.s_id)+ " OR x_traza like '%{0}%' ".format(contract.objid)
        
        if (site):
            strFilter=strFilter + " OR x_traza like '%{0}%' ".format(site.site_id)+ " OR x_traza like '%{0}%' ".format(site.objid)

        if (inputLogin):
            strFilter=strFilter + " OR UPPER(x_traza) like '%{0}%' ".format(inputLogin.upper())
        
        if (inputOTHER):
            strFilter=strFilter + " OR UPPER(x_traza) like '%{0}%' ".format(inputOTHER.upper())
        
        strQuery="""SELECT UPPER('TABLE_X_SC_TRAZAS_WS') AS TABLENAME, '' AS  PACKAGE_NAME , '' AS  BATCHJOB, X_XBEAN AS  ACTION, X_NAME_WS  AS  PROCEDURE_NAME, X_TIME AS TIME, '' AS   PARAMETERS,   ''  AS SQL_CODE, '' AS  ERRMSG, '' AS   LOG_STEP , X_TRAZA AS  COMMENTS,  '' AS  SEQ , '' AS   MENSAJE,  ''  AS CONTRACT_OBJID, '' AS   CONTRACT_ID  
                    FROM    TABLE_X_SC_TRAZAS_WS
                    WHERE   x_time>= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') - INTERVAL  '{1}' MINUTE  
                    AND     x_time<= to_date('{0}','yyyy-mm-dd Hh24:MI:SS') + INTERVAL  '{1}' MINUTE """.format(inputDate, inputGap)
        
        strQuery=strQuery+ "AND ({0}) ".format(strFilter)

        query=smart_query.my_custom_sql('smart_replica', strQuery)
        output.extend(query)


        return sorted(output, key=lambda k:k['time'], reverse=True)


    