from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
import traceback
import json
from core.vodafone.smart.contract.models import Contract
from django.conf import settings
from core.vodafone.smart import smart_query


log = logging.getLogger(__name__)

class ContractValidation:

    def validate(params):

        log.info('Start: validate')

        if not "s_id" in params:
            raise ApiException("Invalid params. s_id required.")
        
        try:
            contract=Contract.objects.get(s_id=params["s_id"])
        except Contract.DoesNotExist:
            raise ApiException ("Contract %s not found" % params["s_id"])
        
        try:
  
            paramsProc=[
                    {
                     "name": "contractobjid",
                     "inout": "IN",
                     "type": "Number",
                     "value": contract.objid
                    },
                    {
                     "name": "resultado",
                     "inout": "OUT",
                     "type": "String"
                    },
                    {
                     "name": "msg",
                     "inout": "OUT",
                     "type": "String"
                    },
                    {
                     "name": "msgDetailed",
                     "inout": "OUT",
                     "type": "String"
                    }
            ] 

            output=smart_query.execProcedure("smart_replica", "SA.PCK_AVERIAS_TOOLS.P_COMPRUEBA_ORDEN_KO", paramsProc)

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

        log.info('End: validate')

        return output
