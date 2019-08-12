import requests
import json
from json_tricks import dumps
import os
from   django.conf import settings
#from .serializers import AveriaHistoricalSerializer
from core.elasticsearch.serializers import ElasticSearchSerializer
from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery
from ApiADA.constantes import Constantes
import traceback


log = logging.getLogger(__name__)

class AveriaHistorical():

    def setAveriaHistorical(averia):
        
        log.info('Start:setAveriaHistorical')

        if ("case" in averia and averia["case"].__class__.__name__ == 'TableCase'):
            idAveria=averia["case"].id_number
        else:
            idAveria=averia["case"]["id_number"]

        if not idAveria:
            raise ApiException("Error invalid parameters, id_number not informed.")

        serializer=ElasticSearchSerializer(data=averia)
        if (not serializer.is_valid()):
            raise ApiException('Data for averia %s is not valid to be inserted in Elastic' % idAveria)

        body=serializer.validated_data
        headers = {'Content-type': 'application/json'}
        action = "/averias_historical/averia/%s" % idAveria
        try:
                url='https://'+ settings.ELK_SERVER + ":" + str(settings.ELK_PORT) + action
                response=requests.put(url=url, headers=headers, data=json.dumps(body), cert=(os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY) ), verify=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))
                if not response.ok:
                    raise ApiException("Error executing the insert/update in ElasticSearch server for averia %s Response %s" % (idAveria, response.content.decode("utf-8")))
        except ApiException as ae:      
                raise ae
        except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing the insert/update in ElasticSearch server for averia %s Error %s" % (idAveria, str(e)))

        log.info('End:setAveriaHistorical')
