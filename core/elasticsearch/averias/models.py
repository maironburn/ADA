import requests
import json
from json_tricks import dumps
import os
from   django.conf import settings
#from .serializers import AveriaSerializer
from core.elasticsearch.serializers import ElasticSearchSerializer
from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery
from ApiADA.constantes import Constantes
import traceback
from core.elasticsearch.averias_historical.models import AveriaHistorical
from django.core.exceptions import ObjectDoesNotExist


log = logging.getLogger(__name__)

class Averia():

 
    def searchAveriaAnalysisDate(searchanalysisDate):
        log.info('Start:searchAveriaAnalysisDate')

        sql={
                "action": "/averias_backlog/averia",
                "body": {
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "analysis_info.analysis_date": {
                                                    "lte": searchanalysisDate.strftime(Constantes.DATETIME_FORMAT)
                                                }
                                            }
                                        }
                                    ]
                                }
                            },   
                            "_source": ["case.id_number", "site.site_id", "analysis_contract.contract.s_id", "analysis_info.analysis_date", "analysis_info.analysis_details", "analysis_info.analysis_type", "analysis_info.tags", "analysis_info.analysis_details.date", "analysis_info.analysis_details.type", "analysis_info.analysis_details.user", "analysis_info.analysis_details.value"]

                        }
            }

        output=CustomElasticSearchQuery.executeSearchDDL(sql)        

        log.info('End:searchAveriaAnalysisDate')
        return output

    def setAveria(averia):
        
        log.info('Start:setAveria')
        serializer=ElasticSearchSerializer(data=averia)
        if (not serializer.is_valid()):
            raise ApiException('Data for averia %s is not valid to be inserted in Elastic' % averia["case"].id_number)

        body=serializer.validated_data
        headers = {'Content-type': 'application/json'}
        action = "/averias_backlog/averia/%s" % averia["case"].id_number
        try:
                url='https://'+ settings.ELK_SERVER + ":" + str(settings.ELK_PORT) + action
                response=requests.put(url=url, headers=headers, data=json.dumps(body), cert=(os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY) ), verify=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))
                if not response.ok:
                    raise ApiException("Error executing the insert/update in ElasticSearch server for averia %s Response %s" % (averia["case"].id_number, response.content.decode("utf-8")))
        except ApiException as ae:      
                raise ae
        except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing the insert/update in ElasticSearch server for averia %s Error %s" % (averia["case"].id_number, str(e)))

        log.info('End:setAveria')


    def moveToHistorical(averia):
        log.info('Start:moveToHistorical')
      
        sql=    {
                    "protocol": "POST",
                    "action": "/averias_backlog/averia/_search",
                    "body": 
                    {
                        "query": 
                        {
                            "bool":
                            {
                                "must": [
                                    {
                                        "term": 
                                        {
                                            "case.id_number": averia
                                        }
                                    }
                                ]
                            }
                        }
                    }
                }
            
        averiaInfo=CustomElasticSearchQuery.executeDDL(sql)
        if ((averiaInfo) and ("hits" in averiaInfo) and ("hits" in averiaInfo["hits"])):
            for averiaDelete in averiaInfo["hits"]["hits"]:
                AveriaHistorical.setAveriaHistorical(averiaDelete["_source"])
                Averia.deleteAveria(averiaDelete["_id"])

        log.info('End:moveToHistorical')



    def deleteAveria(idNumber):
        log.info('Start:deleteAveria')

        #Insertamos el registro en el nuevo índice
        sql={
                "protocol": "DELETE",
                "action": "/averias_backlog/averia/%s" % idNumber,
                "body": {}
            }

        CustomElasticSearchQuery.executeDDL(sql)

        log.info('End:deleteAveria')

    def getAveria(idNumber):
        log.info('Start:getAveria')

         #Insertamos el registro en el nuevo índice
        sql={
                "protocol": "GET",
                "action": "/averias_backlog/averia/%s/_source" % idNumber,
                "body": {}
            }


        averia_info=CustomElasticSearchQuery.executeDDL(sql)
        if ("error" in averia_info):
            if (("reason" in averia_info["error"]) and ("Document not found" in averia_info["error"]["reason"])):
                raise ObjectDoesNotExist(averia_info["error"]["reason"])
            else:
                raise ApiException(averia_info["error"])
        return averia_info
        log.info('End:getAveria')