import requests
import json
import os
from   django.conf import settings
from core.exceptions.customexceptions import ApiException
from ApiADA.constantes import Constantes
from datetime import datetime
import traceback

from ApiADA.loggers import logging
log = logging.getLogger(__name__)



class CustomElasticSearchQuery():

    def executeSQL(sql):
        try:
            output=[]
            url='https://'+ settings.ELK_SERVER + ":" + str(settings.ELK_PORT) + "/_xpack/sql"
            headers = {'Content-type': 'application/json'}
            dataSQL={"query": sql ,  "fetch_size": Constantes.ELK_MAX_RECORDS_COUNT}
            response=requests.post(url=url, headers=headers, data=json.dumps(dataSQL), cert=(os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY) ), verify=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))
            if not response.ok:
                    raise ApiException("Error executing a SQL in ElasticSearch sql: %s response: %s" % (sql, response.content.decode("utf-8")))
            
            data=json.loads(response.content.decode("utf-8"))
            if "columns" in data:
                columns=data["columns"]

            for row in data["rows"]:
                tmpRow={}
                for iCol in range(len(columns)):
                    if columns[iCol]["type"]=="date":
                        tmpRow[columns[iCol]["name"]]=datetime.strptime(row[iCol],Constantes.ELK_DATETIME_FORMAT)
                    else:
                        tmpRow[columns[iCol]["name"]]=row[iCol]

                output.append(tmpRow)

            #Verificamos si hay mas datos, para ello nos fijamos si en el JSON de vuelta tenemos la variable cursor
            moreData= "cursor" in data
            while moreData:
                dataSQL={"cursor": data["cursor"] }
                response=requests.post(url=url, headers=headers, data=json.dumps(dataSQL), cert=(os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY) ), verify=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))
                if not response.ok:
                    raise ApiException("Error executing a SQL in ElasticSearch sql: %s response: %s" % (sql, response.content.decode("utf-8")))
            
                data=json.loads(response.content.decode("utf-8"))
                for row in data["rows"]:
                    tmpRow={}
                    for iCol in range(len(columns)):
                        if columns[iCol]["type"]=="date":
                            tmpRow[columns[iCol]["name"]]=datetime.strptime(row[iCol],Constantes.ELK_DATETIME_FORMAT)
                        else:
                            tmpRow[columns[iCol]["name"]]=row[iCol]

                    output.append(tmpRow)
                moreData= "cursor" in data
            
            return output


        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise e  

    
    def executeSearchDDL(sql):
        return CustomElasticSearchQuery.executeSearchBaseDDL(sql=sql, server=settings.ELK_SERVER, port=str(settings.ELK_PORT), certPem=os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),certKey=os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY), certRootCa=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA), onlySource=True)

    def executeSearchBaseDDL(sql, server, port, certKey, certPem, certRootCa, onlySource=True):
         
        if not "action" in sql:
            raise  ApiException("Action property is required")

        if not "body" in sql:
            raise  ApiException("Body property is required")
         
        try:
            output=[]
            url='https://'+ server + ":" + str(port) + sql["action"] + "/_search?scroll=" + Constantes.ELK_SCROLL_TIME
            headers = {'Content-type': 'application/json'}
            
            dataSQL={"size": Constantes.ELK_MAX_RECORDS_COUNT}
            dataSQL.update(sql["body"])

            response=requests.post(url=url, headers=headers, data=json.dumps(dataSQL), cert=(certPem ,certKey), verify=certRootCa)
            if not response.ok:
                    raise ApiException("Error executing a SQL in ElasticSearch sql: %s response: %s" % (sql, response.content.decode("utf-8")))
            
            data=json.loads(response.content.decode("utf-8"))

            totalNumberOfRecords=data["hits"]["total"]
            if (totalNumberOfRecords==0):
                return output

            for row in data["hits"]["hits"]:
                if (onlySource):
                    output.append(row["_source"])
                else:    
                    output.append(row)
            
            while (len(output)<=totalNumberOfRecords and len(data["hits"]["hits"])>0):
                dataSQL={
                            "scroll": Constantes.ELK_SCROLL_TIME,
                            "scroll_id": data["_scroll_id"]
                        }
                url='https://'+ server+ ":" + str(port) + "/_search/scroll"
                response=requests.post(url=url, headers=headers, data=json.dumps(dataSQL), cert=(certPem ,certKey), verify=certRootCa)
                if not response.ok:
                    raise ApiException("Error executing a SQL in ElasticSearch sql: %s response: %s" % (sql, response.content.decode("utf-8")))
            
                data=json.loads(response.content.decode("utf-8"))

                for row in data["hits"]["hits"]:
                    if (onlySource):
                        output.append(row["_source"])
                    else:    
                        output.append(row)

            #Limpiamos el scroll
            try:
                url='https://'+ server + ":" + str(port) + "/_search/scroll"
                dataSQL={
                            "scroll_id": data["_scroll_id"]
                        }
                response=requests.delete(url=url, headers=headers, data=json.dumps(dataSQL), cert=(certPem ,certKey), verify=certRootCa)
            except:
                pass
            
            return output


        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise e

    def executeDDL(sql):
        return CustomElasticSearchQuery.executeBaseDDL(sql=sql, server=settings.ELK_SERVER, port=str(settings.ELK_PORT), certPem=os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT),certKey=os.path.join(settings.CERTS_FOLDER,settings.ELK_CERT_KEY), certRootCa=os.path.join(settings.CERTS_FOLDER,settings.ELK_ROOT_CA))

    def executeBaseDDL(sql, server, port, certKey, certPem, certRootCa):

        output=None
        log.info('Start:executeDDL')
        if not "protocol" in sql:
            raise  ApiException("Protocol property is required")

        if not "action" in sql:
            raise  ApiException("Action property is required")

        if not "body" in sql:
            raise  ApiException("Body property is required")

        headers = {'Content-type': 'application/json'}


        if sql["protocol"]=="GET":
            try:
                url='https://'+ server + ":" + str(port) + sql["action"]
                response=requests.get(url=url, headers=headers, cert=(certPem,certKey), verify=certRootCa)
              
            except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing a query in ElasticSearch server")

        elif sql["protocol"]=="PUT":
            try:
                url='https://'+ server + ":" + str(port) + sql["action"]
                response=requests.put(url=url, headers=headers, data=json.dumps(CustomElasticSearchQuery.mapJSONData(sql["body"])), cert=(certPem,certKey), verify=certRootCa)
              
            except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing a query in ElasticSearch server")
        
        elif sql["protocol"]=="POST":
            try:
                url='https://'+ server + ":" + str(port) + sql["action"]
                response=requests.post(url=url, headers=headers, data=json.dumps(CustomElasticSearchQuery.mapJSONData(sql["body"])), cert=(certPem,certKey), verify=certRootCa)
              
            except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing a query in ElasticSearch server")   
        
        elif sql["protocol"]=="DELETE":
            try:
                url='https://'+ server + ":" + str(port) + sql["action"]
                response=requests.delete(url=url, headers=headers, cert=(certPem,certKey), verify=certRootCa)
              
            except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException("Error executing a query in ElasticSearch server")                                 
        else:
            raise  ApiException("Invalid protocol:"+sql["protocol"])

        if ("text/plain" in response.headers['content-type']):
            output={"response":response.content.decode("utf-8")}
        elif ("application/json" in response.headers['content-type']):
            output=json.loads(response.content.decode("utf-8"))
        
        log.info('End:executeDDL')
        return output

    def mapJSONData(data):
        if data.__class__.__name__ == 'str':
            return json.loads(data)
        else:
            return data    
        

 