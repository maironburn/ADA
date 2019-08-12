from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from core.vodafone.smart.contract.models import Contract
from core.vodafone.smart.site.models import Site
from datetime import datetime
from core.vodafone.smart import smart_query
from core.beans.analysis_contract.analysis_contract import AnalysisContract
from clasification.models import Clasification

log = logging.getLogger(__name__)

class ClasifyAveria:

    def clasifyContract(parameters) :

        log.info('Start: clasifyContract')

        if (not parameters):
            raise ApiException("Invalid parameters.")
        
        if (not "inputOT" in parameters):
            raise ApiException("Invalid parameter. inputOT is mandatory")
        

        try:
            contract=Contract.objects.get(s_id=parameters["inputOT"])
        
        except Contract.DoesNotExist: 
            raise ApiException("Invalid parameter. %s Contract not found" % parameters["inputOT"])

        query_contract = """select c.s_id, c.title, c.s_title, st.site_id, NVL(clas.objid, '') as objidxclasorden, NVL(clas.x_clasificacion,'') as x_clasificacion, NVL(clas.x_descripcion,'') as x_descripcion 
                        from sa.table_contract c, 
                                sa.table_contr_schedule cs, 
                                sa.table_site st, 
                                sa.table_x_clas_orden clas
                        where c.s_id= '%s' 
                        and c.objid=cs.schedule2contract
                        and cs.ship_to2site=st.objid 
                        and clas.objid = c.x_contract2x_clas_orden """ % (contract.s_id)

        queryContract=smart_query.my_custom_sql('smart_gg', query_contract)
        if (len(queryContract)==0):
            raise ApiException("Invalid parameters. Contract %s not found." % contract.s_id)
        else:    
            try:
                if ((not queryContract[0]["objidxclasorden"]) or (queryContract[0]["objidxclasorden"]==0)):
                    return Clasification.TYPE_CONTRACT_NOT_DEFINED
                elif (queryContract[0]["title"].upper()!=queryContract[0]["x_descripcion"].upper()):
                    return Clasification.TYPE_CONTRACT_WRONG_NAMED
                return Clasification.TYPE_CONTRACT_IN_PROGRESS

            except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException(str(e))





