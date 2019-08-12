from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
import traceback
import json
from core.vodafone.smart.contract.models import Contract
from django.conf import settings
from core.vodafone.smart import smart_query


log = logging.getLogger(__name__)

class AveriasManagement:

    def AddComment(params):

        log.info('Start: AddComment')

        if not "s_id_averia" in params:
            raise ApiException("Invalid params. s_id_averia required.")
        if not "s_user" in params:
            raise ApiException("Invalid params. s_user required.")

        try:
  
            paramsProc=[
                    {
                     "name": "id_averia",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_id_averia"]
                    },
                    {
                     "name": "usuario",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_user"]
                    },
                    {
                     "name": "comentario",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_comentario"]
                    },
                    {
                     "name": "id_incidencia",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_id_incidencia"]
                    },
                    {
                     "name": "resultado",
                     "inout": "OUT",
                     "type": "String"
                    },
                    {
                     "name": "res_desc",
                     "inout": "OUT",
                     "type": "String"
                    }
            ] 

            output=smart_query.execProcedure("smart_replica", "SA.PKG_GESTION_AVERIAS_ADA.PRC_ADD_COMENTARIO_AVERIA", paramsProc)

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

        log.info('End: AddComment')

        return output


    def MoveAveria(params):

        log.info('Start: MoveAveria')

        if not "s_id_averia" in params:
            raise ApiException("Invalid params. s_id_averia required.")
        if not "s_queue" in params:
            raise ApiException("Invalid params. s_queue required.")

        try:
  
            paramsProc=[
                    {
                     "name": "id_averia",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_id_averia"]
                    },
                    {
                     "name": "cola_destino",
                     "inout": "IN",
                     "type": "Number",
                     "value": params["s_queue"]
                    },
                    {
                     "name": "resultado",
                     "inout": "OUT",
                     "type": "String"
                    },
                    {
                     "name": "res_desc",
                     "inout": "OUT",
                     "type": "String"
                    }
            ] 

            output=smart_query.execProcedure("smart_replica", "SA.PKG_GESTION_AVERIAS_ADA.PRC_MOVER_AVERIA_A_NUEVA_COLA", paramsProc)

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

        log.info('End: MoveAveria')

        return output


    def CloseAveria(params):

        log.info('Start: CloseAveria')

        if not "s_id_averia" in params:
            raise ApiException("Invalid params. s_id_averia required.")
        if not "s_notes" in params:
            raise ApiException("Invalid params. s_notes required.")

        try:
  
            paramsProc=[
                    {
                     "name": "id_averia",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_id_averia"]
                    },
                    {
                     "name": "strnotas",
                     "inout": "IN",
                     "type": "String",
                     "value": params["s_notes"]
                    },
                    {
                     "name": "resultado",
                     "inout": "OUT",
                     "type": "String"
                    },
                    {
                     "name": "res_desc",
                     "inout": "OUT",
                     "type": "String"
                    }
            ] 

            output=smart_query.execProcedure("smart_replica", "SA.PKG_GESTION_AVERIAS_ADA.PRC_CERRAR_AVERIA", paramsProc)

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

        log.info('End: CloseAveria')

        return output