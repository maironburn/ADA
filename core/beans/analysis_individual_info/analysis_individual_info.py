from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from  django.conf import settings
from core.vodafone.smart.case.models import TableCase
from core.vodafone.smart.site.models import Site
import traceback
import json
from json_tricks import dumps
from django.core.exceptions import ObjectDoesNotExist
from core.elasticsearch.averias.models import Averia
from core.beans.analysis_case.analysis_case import AnalysisCase
from clasification.models import Clasification
from datetime import datetime

log = logging.getLogger(__name__)

class AnalysisIndividualInfo:

    #   Metodo para obtener el site a partir de una averia
    #   inputs:
    #       params: dict con los parametros del procedimiento.
    #           id_number - identificador de la averia
    #
    #   output:
    #       return Site site asociado a la averia
    #
    def getSitefromAveria(params):
        log.info('Start:getSitefromAveria')
        if (not "id_number" in params):
            raise ApiException("Invalid parameters. Id_number is required")
        try:
            
            try:
                averia=TableCase.objects.get(id_number=params["id_number"])
            except TableCase.DoesNotExist:
                raise ApiException('Averia %s not found.' % params["id_number"])

            try:    
                site=Site.objects.get(objid=averia.case_reporter2site)
            except Site.DoesNotExist:    
                raise ApiException('Unable to get the site related to Averia %s.' % params["id_number"])

            log.info('End:getSitefromAveria')
            return site

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))


    #   Metodo para obtener a partir de una averia la clasificacion de la averia
    #   inputs:
    #       params: dict con los parametros del procedimiento.
    #           id_number - identificador de la averia
    #           site_id - identificador del site (opcional)
    #   output:
    #       return Clasification  asociado a la averia
    #
    def getAnalysisDetailsFromAveria(params):
        log.info('Start:getAnalysDetailsFromAveria')
        if (not "id_number" in params):
            raise ApiException("Invalid parameters. Id_number is required")
        try:    
            try:
                averia=Averia.getAveria(params["id_number"])    

                if (averia["analysis_info"][ "analysis_type"]=='Manual'):
                    return averia["analysis_info"]
            except ObjectDoesNotExist:
                pass
            
            try:
                averia=TableCase.objects.get(id_number=params["id_number"])
            except TableCase.DoesNotExist:
                raise ApiException('Averia %s not found.' % params["id_number"])   

            if ("site_id" in params):
                try:
                    site=Site.objects.get(site_id=params["site_id"])
                except Site.DoesNotExist:    
                    raise ApiException('Site %s not found.' % params["site_id"])
            else:           
                try:    
                    site=Site.objects.get(objid=averia.case_reporter2site)
                except Site.DoesNotExist:    
                    raise ApiException('Unable to get the site related to Averia %s.' % params["id_number"])

            output=AnalysisCase.analyzeComments(site=site, comments=averia.getCommentsWorklog(), text=None)
            log.info('End:getAnalysDetailsFromAveria')
            return output

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))
    
    #   Metodo para obtener a partir de una averia la clasificacion de la averia
    #   inputs:
    #       params: dict con los parametros del procedimiento.
    #           id_number - identificador de la averia (opcional)
    #           site_id - identificador del site (opcional)
    #           analysis_details - objeto a analizar
    #   output:
    #       return Clasification  asociado a la averia
    #
    def getAnalysisDetailsFromText(params):
        log.info('Start:getAnalysDetailsFromText')
        if (not "analysis_details" in params):
             raise ApiException('Invalid parameters. analysis_details is required.')   
    
        if (not "text" in params["analysis_details"] or params["analysis_details"]["text"].strip()==''):
             raise ApiException('Invalid parameters. analysis_details.text is required.')   

        if (not "type" in params["analysis_details"] or params["analysis_details"]["type"].strip()==''):
             raise ApiException('Invalid parameters. analysis_details.type is required.')   
        
    
        averia=None
        if ("id_number" in params):           
            try:
                averia=TableCase.objects.get(id_number=params["id_number"])
            except TableCase.DoesNotExist:
                raise ApiException('Averia %s not found.' % params["id_number"])   

        site=None
        if ("site_id" in params):
            try:
                site=Site.objects.get(site_id=params["site_id"])
            except Site.DoesNotExist:    
                raise ApiException('Site %s not found.' % params["site_id"])
        elif (averia):           
            try:    
                site=Site.objects.get(objid=averia.case_reporter2site)
            except Site.DoesNotExist:    
                raise ApiException('Unable to get the site related to Averia %s.' % averia.id_number)

        try:    
            if (params["analysis_details"]["type"] in [Clasification.TYPE_CONTRACT_IN_PROGRESS,
                                                       Clasification.TYPE_INTERNAL_ERROR,
                                                       Clasification.TYPE_CONTRACT_NOT_DEFINED,
                                                       Clasification.TYPE_CONTRACT_WRONG_NAMED] ):

                output=AnalysisCase.analyzeComments(text=params["analysis_details"]["text"], site=site, comments=[])

            if (not output):
                    output=params["analysis_details"]
                    output["date"]=datetime.now()
                    output["value"]=output["text"]

            log.info('End:getAnalysDetailsFromText')
            return output

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))
   