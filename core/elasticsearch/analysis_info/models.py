import requests
import json
from json_tricks import dumps
import os
from   django.conf import settings
from .serializers import AnalysisInfoSerializer
from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery
from ApiADA.constantes import Constantes
import traceback


log = logging.getLogger(__name__)

class AnalysisInfo():

    def setAnalysisInfo(data):
        
        log.info('Start:AnalysisInfo')

        serializer=AnalysisInfoSerializer(data=data)
        if (not serializer.is_valid()):
            raise ApiException('Data for AnalysisInfo is not valid.' )

        body=serializer.validated_data
        headers = {'Content-type': 'application/json'}
        action = "/analysis_info/analysis/"+data["queue"]
        try:
                url='https://'+ settings.ELK_SERVER + ":" + str(settings.ELK_PORT) + action
                response=requests.put(url=url, headers=headers, data=json.dumps(body), cert=(os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY) ), verify=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))
                if not response.ok:
                    raise ApiException("Error executing the insert/update in ElasticSearch server for AnalysisInfo Response %s" % (response.content.decode("utf-8")))
        except ApiException as ae:      
                raise ae
        except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing the insert/update in ElasticSearch server for AnalysisInfo Error %s" % (str(e)))

        log.info('End:AnalysisInfo')
