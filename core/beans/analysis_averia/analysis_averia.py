from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from appparameter.models import Appparameter
from core.vodafone.smart.queue.models import TableQueue
from core.vodafone.smart.site.models import Site
from core.vodafone.smart.case.models import TableCase
from datetime import datetime, timedelta
import pytz
import dateutil.parser
from core.beans.rules_engine.rulesetAux import RulesetAux
from core.beans.analysis_case.analysis_case import AnalysisCase
from core.beans.analysis_contract.analysis_contract import AnalysisContract
from core.elasticsearch.averias.models import Averia
from core.elasticsearch.analysis_info.models import AnalysisInfo
from analysiserror.models import Analysiserror
from  django.conf import settings
import traceback
import json
from json_tricks import dumps
from core.beans.customer_validation.customer_validation import CustomerValidation
from core.beans.contract_validation.contract_validation import ContractValidation
from core.beans.asset_validation.asset_validation import AssetValidation
from auditprocess.models import Auditprocess
from threading import Thread
import queue
from django.core.exceptions import ObjectDoesNotExist
from core.beans.rules_engine.ruleset import RulesetImplementation
from ruleset.models import Ruleset
from clasification.models import Clasification


log = logging.getLogger(__name__)

class AnalysisAveria:

    tmpqueue=queue.Queue()


    ####################################################################################################
    #   Metodo que realizar el analisis de las averías que se encuentre en backlog, para todas las 
    #   colas parametrizadas.
    #
    #   inputs:
    #       params: array con los parametros del procedimiento. (Actualmente no se requiere ninguno)
    #               Array de objetos JSON con format (Ejemplo de JSON)
    #               {
    #                       "name": Nombre del parametro
    #                       "inout": Direccion del parametro IN para parametros de entrada OUT para parametros de salida
    #                       "type": Tipo de dato (String o Number) 
    #                       "vallue": Valor del parametro (solo para los parametros de entrada)
    #               } 
    #       auditprocess: Objeto de auditoria (opcional)   
    #   output:
    #       return dict con los datos obtenidos en el análisis realizado, para cada una de las averías.
    #
    ####################################################################################################
    def analyzeBacklog(params, auditprocess=None):
        log.info('Start:analyzeBacklog')


        try:
            
            #Averia.getAveria()
            #return []
            RulesetAux.setFieldPatternValidator()
            datenow=datetime.now()
            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()
            
            output=[]

            if (auditprocess):
                auditprocess.setInProgress({"initial_records":0})

            for queue in queue_list:
                queue_value=queue['queue']
                if ("datebacklog" in queue and queue["datebacklog"] and queue["datebacklog"].strip()!=""):
                    datebacklog=dateutil.parser.parse(queue['datebacklog'])
                    timegapbacklog_param=Appparameter.objects.get(name='time gap backlog')
                    timegapbacklog=timegapbacklog_param.getParamaterDataValue()

                    searchdate=datebacklog - timedelta(minutes=int(timegapbacklog))
                else:
                    utc=pytz.UTC
                    searchdate=utc.localize(datetime.min)   
                


                if (not params):
                    params={}

 
                params.update({"queue": queue_value,"searchdate": searchdate}), 

                output.extend(AnalysisAveria.analyzeBacklogQueue(params, auditprocess))
            

            if (auditprocess):
                auditprocess.setFinished({"final_records":len(output)})

            log.info('End:analyzeBacklog')
            return output

        except Exception as e:
            if (auditprocess):
                auditprocess.setError({"msg":str(e)})
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

  
    ####################################################################################################
    #   Metodo que realizar el analisis de las averías que se encuentre en backlog, para todas las 
    #   colas parametrizadas.
    #
    #   inputs:
    #       params: array con los parametros del procedimiento. 
    #               "queue"  cola a analizar
    #               "searchdate"   fecha a partir de la cual obtener los datos
    #       auditprocess: Objeto de auditoria (opcional)   
    #   output:
    #       return dict con los datos obtenidos en el análisis realizado, para cada una de las averías.
    #
    ####################################################################################################
    def analyzeBacklogQueue(params, auditprocess=None):
        
        log.info('Start:analyzeBacklogQueue')


        if (not "queue" in params):
            raise ApiException("Invalid parameters. Queue not informed")
        if (not "searchdate" in params):
            raise ApiException("Invalid parameters. Searchdate not informed")


        try:
            
            #Averia.getAveria()
            #return []
            RulesetAux.setFieldPatternValidator()
            datenow=datetime.now()
            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()
            queues=TableQueue.objects.filter(s_title__in=list(map(lambda x: x["queue"].upper(), queue_list))).all()
            
            try:                
                queue=TableQueue.objects.get(s_title=params["queue"].upper())
            except  TableQueue.DoesNotExist:
                return []   
          
            output=[]

            # ESTE ES EL BUENO
            searchdate=params["searchdate"]
            log.info('Execute search queue: '+queue.s_title+' from date:' + str(searchdate))
            cases=TableCase.objects.filter(modify_stmp__gte=searchdate).filter(case_currq2queue=queue.objid)
            #cases=TableCase.objects.filter(case_currq2queue__in=queue_list_objid)
            #Lista_cases=['80255228','76928587','76662562','77779147','77918161','78658372','78624827','78979750','79099490','79034307','79158518','79204217','79509526','79223943','79293245','79369298','79374503','79478501','79660000','79626937','79745203','79761425','79869976','79929839','80002439','80044578','80035593','80050901','80096225','80084625','80021600','80123873','80153614','80110353','80131204','80128846','80189657','80261960','80285417','80341623','80488398','80444731','80560624','80521494','80599357','80708961','79611974','80379073','79920073','79699596','79777464','80249699','79879150','79746444','79770851','80122269','78392440','78724984','78918894','79114271','79169994','79655427','79133632','79563780','79413623','79700809','79824162','79906640','79773140','79818966','79799013','79661906','79936864','79903940','80460821','79962637','79862006','80026021','80014565','79893729','80112776','80045882','80046057','79948253','80162021','80465448','80138137','80150732','80162891','80245634','80238879','80057027','80352504','80296930','80338774','80315209','80329875','80314719','80124866','80358290','80509323','80023836','80451860','80590750','80574297','80279342','80286735','80825210','80137706','80102703','80795721','80214019','80182556','80512130','80220896','80683477','80463457','80852392','80077718','79850945','79000162','79716993']
            #cases=TableCase.objects.filter(id_number__in=Lista_cases)
            #cases=cases[1:5]
            log.info('Query executed, number of results:'+ str(len(cases)))

            if (len(cases)==0):                
                AnalysisInfo.setAnalysisInfo({"last_analysis_date":datenow, "queue":queue.s_title.upper()}) 
                return []
            else:
                numberThreads_param=Appparameter.objects.get(name__iexact='Number of threads')
                numberThreads=int(numberThreads_param.getParamaterDataValue())
            
                max_date=None

                casesList=[]
                numberOfListThreads=int(len(cases)/numberThreads)
                i=0
                for initElement in range(numberThreads-1):
                    casesList.append(cases[i*numberOfListThreads: (i+1)*numberOfListThreads])           
                    i=i+1

                casesList.append(cases[i*numberOfListThreads:])

                threads = []
                for elemThread in range(numberThreads):
                    threads.append(PropagatingThread(target=AnalysisAveria.manageBacklogCases, args=(queues,casesList[elemThread])))
                    threads[-1].start()

                for thread in threads:
                    #thread.join() 
                    try:
                        thread.join()
                        queue_data=AnalysisAveria.tmpqueue.get()   
                        max_date=queue_data["max_date"] if not max_date else max([queue_data["max_date"], max_date])                        
                        output.extend(queue_data["events"])
                    except Exception as ex:  
                        log.error('Exception:'+type(ex).__name__ +" " +str(ex))
                        log.error(traceback.format_exc())
                        raise ex
             
            AnalysisInfo.setAnalysisInfo({"last_analysis_date":datenow, "queue": queue.s_title.upper(), "last_case_timestamp":max_date})   

            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()

            for i,item in enumerate(queue_list):
                if (item["queue"].upper()==queue.s_title.upper() and ((not "datebacklog" in item) or (item["datebacklog"].strip()=="") or  (max_date > dateutil.parser.parse(item["datebacklog"])) ) ): 
                    queue_list[i]={"queue":queue.s_title.upper(), "datebacklog":max_date.isoformat()}            

            queue_list_param.setParameterDataValue(queue_list)
            queue_list_param.save()  

            log.info('End:analyzeBacklogQueue')
            return output

        except Exception as e:
            if (auditprocess):
                auditprocess.setError({"msg":str(e)})
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

    ####################################################################################################
    # Método que se ejecutara cada 3 horas, que recogera todas aquellas averias que se encuentren 
    # en el ELK, desde una determinada fecha, para analizar si todavía continuan en backlog, o no.
    # Si la avería no continua en backlog, internamente se historificara, y en el caso contrario, se
    # actualizará la información de la avería.
    # 
    # También permite la opción de obtener el número de averias pertenecientes al ELK, que se encuentran
    # en backlog, sin realizaar su correspondiente análisis.
    #
    # input:
    #           params: 
    #                   analyze_event: Parametro que indica si es necesario realizar el análisis o no, de 
    #                                  aquellas averias que se encuentran en backlog.
    #                                   true - Mueve las averias no en backlog al historico y con las averias de backlog las analiza
    #                                   false - Solo Mueve las averias no en backlog al historico
    #           auditprocess: Objeto de auditoria (opcional) 
    # output:
    #           output: Contendría las averias en backlog actualizadas, en el caso que proceda, o solo el
    #                   número de averias en backlog.
    #
    #####################################################################################################
    def analyzeElastic(params, auditprocess=None):

        log.info('Start:analyzeElastic')

        RulesetAux.setFieldPatternValidator()

        if ("analyze_event" in params):
            analyze_event=params["analyze_event"]

        else:
            analyze_event=False

        
        try:
            

  
            numberThreads_param=Appparameter.objects.get(name__iexact='Number of threads')
            numberThreads=int(numberThreads_param.getParamaterDataValue())
            
            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()
            
            queues=TableQueue.objects.filter(s_title__in=list(map(lambda x: x["queue"].upper(), queue_list))).all()
            
            output=[]

            if (analyze_event):
                timegapbacklog_param=Appparameter.objects.get(name='time gap analysis')
                timegapbacklog=timegapbacklog_param.getParamaterDataValue()
                searchdate=datetime.now() - timedelta(minutes=int(timegapbacklog))
            else:
                searchdate=datetime.now()   

         
            elkCases=Averia.searchAveriaAnalysisDate(searchdate)
            if (auditprocess):
                auditprocess.setInProgress({"initial_records": len(elkCases)})

            if (len(elkCases)>0):
               
                elkCasesList=[]
                numberOfListThreads=int(len(elkCases)/numberThreads)
                i=0
                for initElement in range(numberThreads-1):
                    elkCasesList.append(elkCases[i*numberOfListThreads: (i+1)*numberOfListThreads])           
                    i=i+1

                elkCasesList.append(elkCases[i*numberOfListThreads:])

                threads = []
                for elemThread in range(numberThreads):
                    threads.append(PropagatingThread(target=AnalysisAveria.manageELKCases, args=(searchdate,queues,elkCasesList[elemThread],analyze_event)))
                    threads[-1].start()

                for thread in threads:
                    #thread.join() 
                    try:
                        thread.join()
                        queue_data=AnalysisAveria.tmpqueue.get()                           
                        output.extend(queue_data["events"])
                    except Exception as ex:  
                        log.error('Exception:'+type(ex).__name__ +" " +str(ex))
                        log.error(traceback.format_exc())
                        raise ex  
                
                if (auditprocess):
                    auditprocess.setFinished({"final_records":len(output)})
            else:
                if (auditprocess):
                    auditprocess.setFinished({"final_records":0})
                      
            log.info('End:analyzeElastic')
            return output

        except Exception as e:
            if (auditprocess):
                auditprocess.setError({"msg":str(e)})
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            log.info('End:analyzeElastic')
            raise ApiException(str(e))


    ####################################################################################################
    # Método que se encarga de encolar temporalmente la información que va obteniendo cada uno de los
    # hilos que se han lanzado. 
    #
    # input:
    #           params: 
    #                   f: es una parametro interno que hace referencia al hilo que esta procesando.
    # output:
    #           output:
    #                   wrapper: parametro interno de python, con la información de gestión del hilo. 
    #
    #####################################################################################################
    def storeInQueue(f):
        def wrapper(*args):
            AnalysisAveria.tmpqueue.put(f(*args))
        return wrapper


    ###############################################################################################
    # Método de realizar el analisis de las averias pasadas por parametro
    # input:
    #           params: 
    #                   queues: Las colas para las que se estan analizando las averias. 
    #                   listCases: Conjunto de Averias a analizar
    # output:
    #           output: Contendría las averias actualizadas, que se han a aanlizar.
    #
    ################################################################################################
    @storeInQueue
    def manageBacklogCases(queues, listCases):
        log.info('Start:manageBacklogCases')
        output=[]
    
        utc=pytz.UTC
        max_date= utc.localize(datetime.min) 
        
        for case in listCases:
                try:
                    event=None
                    averia=Averia.getAveria(case.id_number)    

                    if (averia["analysis_info"][ "analysis_type"]=='Manual'):
                        event=AnalysisAveria.analyzeCaseManualBacklog(case=case, site_id=averia["site"]["site_id"], analysis_info=averia["analysis_info"], queues=queues)
                    elif (averia["analysis_info"][ "analysis_type"]=='Automatic'):
                        event=AnalysisAveria.analyzeCaseAutomaticBacklog(case, queues)
                except ObjectDoesNotExist:
                    event=AnalysisAveria.analyzeCaseAutomaticNotBacklog(case, queues)
                

                if (event):
                    output.append(event)
                    max_date=event["case"].modify_stmp if not max_date else max([event["case"].modify_stmp, max_date])

        log.info('End:manageBacklogCases')
        return {"events":output, "max_date":max_date}



    ###############################################################################################
    # Método que se encarga de recuperar del ELK (elasticsearch), toda la información de
    # las averías que le hayan llegado en la entrada.
    # Con la información oobtenida, dicriminará si se tiene que hacer una análisis manual o
    # automático, para cada una de las incidencias. Obtenieno como resultado la actualización
    # de las mismas.
    #
    # input:
    #           params: 
    #                   searchDate: fecha de referencia para recuperar las averias. 
    #                   queues: Las colas para las que se estan analizando las averias. 
    #                   listCases: Conjunto de Averias que se tomarían como base a buscar en el ELK
    # output:
    #           output: Contendría las averias actualizadas, que se han a aanlizar.
    #
    ################################################################################################
    @storeInQueue
    def manageELKCases(searchDate, queues, listCases, analyze_event):
        log.info('Start:manageELKCases')
        averias=AnalysisAveria.getElasticCurrentBacklog({"searchDate":searchDate, "queues":queues, "elkCases":listCases})
        output=[]
        utc=pytz.UTC
        max_date= utc.localize(datetime.min) 
        if (analyze_event):
            for averia in averias:
                try:
                    event=None

                    if (averia["analysis_info"][ "analysis_type"]=='Manual'):
                        event=AnalysisAveria.analyzeCaseManualBacklog(case=averia["case"], site_id=averia["site"]["site_id"], analysis_info=averia["analysis_info"], queues=queues)
                    elif (averia["analysis_info"][ "analysis_type"]=='Automatic'):
                        event=AnalysisAveria.analyzeCaseAutomaticBacklog(averia["case"], queues)

                    if (event):
                        output.append(event)
                        max_date=event["case"].modify_stmp if not max_date else max([event["case"].modify_stmp, max_date])
                except:
                     pass

            log.info('End:manageELKCases')
            return {"events":output, "max_date":max_date}
        else:
            log.info('End:manageELKCases')
            return {"events":listCases, "max_date":datetime.min}


    #Metodo revison averias elasticsearch antes del analisis
    ########################################################################
    # Método para obtener todas aquellas incidencias provenientes del ELK
    # que se encuentran todavía en backlog, y para las cuales se tendría que
    # que volver a realizar su análisi, para actualizar la información.
    #
    # Todas aquellas averias que no se encuentren en backlog, se historificaran
    # insertando un registro en la tabla averias_historical y borrando el correspondiente
    # en la tabla averias_backlog.
    #
    # input:
    #           params: 
    #                   searchDate: fecha de referencia para recuperar las averias. 
    #                   queues: Las colas para las que se estan analizando las averias. 
    #                   elkCases: Conjunto de Averias que se tomarían como base a anlizar
    # output:
    #           backlogCases: Contendría las averias que continuan en backlog y para las cuales,
    #                         habría que volver a realizar su análisis.
    #
    #########################################################################
    def getElasticCurrentBacklog(params):
        try:
            log.info('Start:getElasticCurrentBacklog')


            if ("searchDate" in  params):
                searchDate=params["searchDate"]
            else:
                searchDate=datetime.now()

            if ("queues" in params):
                queues=params["queues"] 
            else:
                queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
                queue_list=queue_list_param.getParamaterDataValue()
                    
                queues=TableQueue.objects.filter(s_title__in=list(map(lambda x: x["queue"].upper(), queue_list))).all()   

            if ("elkCases" in params):
                elkCases=params["elkCases"]
            else:   
                elkCases=Averia.searchAveriaAnalysisDate(searchDate)

  

            #Con los id de averias obtenidos, hacemos una consulta por id_number y cola actual en el listado de queue_list
            backlogCases=[]
            backlogCasesIdNumber=[]
            queue_list_objid=list(map(lambda x: x.objid, queues))
            initNumberCasesTotal=len(elkCases)
            getCasesBacklog=True
            initNumberCasesPartial=0
            while getCasesBacklog:
                casesExtended=[]
                partialListCase=elkCases[initNumberCasesPartial:initNumberCasesPartial+1000]
                partialListCaseIdNumber=list(map(lambda x: x["case"]["id_number"], partialListCase))
                cases=TableCase.objects.filter(case_currq2queue__in=queue_list_objid).filter(id_number__in=partialListCaseIdNumber).all()
                backlogCasesIdNumber.extend(list(map(lambda x: x.id_number, cases)))
                for case in cases:  
                    case_initial_list=list(filter(lambda x : x["case"]["id_number"]==case.id_number,partialListCase))
                    for case_initial in case_initial_list:   
                        case_tmp=case_initial.copy()
                        case_tmp["case"]=case
                        casesExtended.append(case_tmp)
                backlogCases.extend(casesExtended)
                initNumberCasesPartial=initNumberCasesPartial+1000
                getCasesBacklog= initNumberCasesPartial <= initNumberCasesTotal

            elkCasesIdNumber=list(map(lambda x: x["case"]["id_number"], elkCases))
            deleteCases=[val for val in elkCasesIdNumber if not val in backlogCasesIdNumber]
            #print("elkCases:"+','.join(elkCases))
            #print("backlogCasesIdNumber:"+','.join(backlogCasesIdNumber))
            for deleteCase in deleteCases:
                try:
                    Averia.moveToHistorical(deleteCase)
                except Exception as e:
                    try:
                        analysisError=Analysiserror.objects.get(averia=deleteCase)
                    except Analysiserror.DoesNotExist:
                        analysisError=Analysiserror()

                    analysisError.averia=case.id_number
                    analysisError.event=None
                    analysisError.modified_date=datetime.now()
                    error={"source":"getElasticCurrentBacklog", "msg": str(e),  "backtrace":  traceback.format_exc()}
                    log.info("Error: "+dumps(error))
                    analysisError.error=dumps(error)
                    analysisError.save()    


            log.info('End:getElasticCurrentBacklog')
            return backlogCases

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))


    ########################################################################
    # Metodo para analizar las validaciones para una determinada OT (contract)
    #
    # input:
    #           params: 
    #                   s_id: identificador de la orden a analizar
    # output:
    #           event: evento generado con la siguinte información
    #               "contract_validation"
    #########################################################################
    def analyzeContract(params):
        if (not "s_id" in params):
            raise ApiException("Invalid parameters. s_id is required")
        try:
            
            event={}    
            log.info('Start:analyzeContract:'+params["s_id"])   

            log.info('Execute contract_validation s_id:'+params["s_id"])       
            event["contract_validation"]=ContractValidation.validate({"s_id": params["s_id"]})

            log.info('Analyze contract s_id:'+params["s_id"])       
            event['analysis_contract']=AnalysisContract.analyze({'contract':params["s_id"]})

            log.info('End:analyzeContract:'+params["s_id"])  
            return event

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))


    ########################################################################
    # Metodo para analizar las validaciones para un determinado Site
    #
    # input:
    #           params: 
    #                   site_id: identificador del cliente a analizar
    # output:
    #           event: evento generado con la siguinte información
    #               "customee_validation"
    #               "asset_validation"
    #########################################################################
    def analyzeSite(params):
        if (not "site_id" in params):
            raise ApiException("Invalid parameters. site_id is required")
        try:
            
            event={}    
            log.info('Start:analyzeSite:'+params["site_id"])   

            event["customer_validation"]=CustomerValidation.validate({"site_id": params["site_id"]})
            event["asset_validation"]=AssetValidation.validate({"site_id": params["site_id"]})

            log.info('End:analyzeSite:'+params["site_id"])  
            return event

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

    #############################################################################
    # Metodo para analizar una averia de forma automatica, cuando no se encuentra
    # en el backlog actual del ELK
    #
    # input:
    #           case: averia a analizar
    #           queues: listado de colas que forman el backlog actual
    # output:
    #           event: evento generado
    ##############################################################################
    def analyzeCaseAutomaticNotBacklog(case, queues):
        try:
            log.info('Start:analyzeCaseAutomaticNotBacklog:'+case.id_number)       
            event={
                    "analysis_info": {
                                        "analysis_type":'Automatic',
                                        "analysis_date":datetime.now()
                                        }
                    }       

          
            event['case']=case
  

            try:
                event["site"]=Site.objects.get(objid= event["case"].case_reporter2site)
            except Site.DoesNotExist:
                event["site"]=None    

            if len(list(filter(lambda x: x.objid == event['case'].case_currq2queue, queues)))>0:
                event['queue']=list(filter(lambda x: x.objid == event['case'].case_currq2queue, queues))[0] 
            else:
                try:
                    event["queue"]=TableQueue.objects.get(objid=event["case"].case_currq2queue)    
                except  TableQueue.DoesNotExist: 
                    event["queue"]=None

            event['analysis_info']['analysis_details']={}
            tmpAnalysis=AnalysisCase.analyzeComments(site=event['site'], comments=event['case'].getCommentsWorklog(), text=None)
            if (tmpAnalysis):
                    event['analysis_info']['analysis_details']=tmpAnalysis

            event['analysis_info']['analysis_details']['user']= event['case'].id_number
            event['analysis_info']['tags']=AnalysisCase.analyzeCommentsPatterns(event['case'].case_history)

            analysis_values=event['analysis_info']['analysis_details']


            if ( "site" in event and event["site"] and  event["site"].site_id):
                event.update( AnalysisAveria.analyzeSite({"site_id": event["site"].site_id}))    

            if (analysis_values and ('type' in analysis_values) and (analysis_values['type']==Clasification.TYPE_CONTRACT_IN_PROGRESS)):
                event.update(AnalysisAveria.analyzeContract({"s_id":analysis_values['value']}))

            AnalysisAveria.evaluateAveria(event)
            AnalysisAveria.performAveria(event)

            #Solo ponemos la averia en el ELK, si la cola del evento esta en el listado de colas que se le pasa al parametro
            if len(list(filter(lambda x: x.objid == event["case"].case_currq2queue, queues)))>0:
               Averia.setAveria(event)


            log.info('End:analyzeCaseAutomaticNotBacklog:'+case.id_number) 
            return event


        except Exception as e:
            try:
                analysisError=Analysiserror.objects.get(averia=case.id_number)
            except Analysiserror.DoesNotExist:
                analysisError=Analysiserror()

            analysisError.averia=case.id_number
            analysisError.event=dumps(event)
            analysisError.modified_date=datetime.now()
            error={"source":"analyzeCaseAutomaticNotBacklog", "msg": str(e),  "backtrace":  traceback.format_exc()}
            log.info("Error: "+dumps(error))
            analysisError.error=dumps(error)
            analysisError.save()
            log.info('End:analyzeCaseAutomaticNotBacklog:'+case.id_number)
            return None

    ###########################################################################
    # Metodo para analizar una averia de forma automatica, cuando se encuentra
    # en el backlog actual del ELK
    #
    # input:
    #           case: averia a analizar
    #           queues: listado de colas que forman el backlog actual
    # output:
    #           event: evento generado
    ###########################################################################
    def analyzeCaseAutomaticBacklog(case, queues):
        log.info('Start:analyzeCaseAutomaticBacklog:'+case.id_number) 
        event=AnalysisAveria.analyzeCaseAutomaticNotBacklog(case, queues)
        log.info('End:analyzeCaseAutomaticBacklog:'+case.id_number) 
        return event     
        

    ########################################################################
    # Metodo para analizar una averia de forma Manual, cuando ya se encuentra
    # en el backlog actual del ELK
    #
    # input:
    #           params: parametros de entrada
    #               case: objeto de la averia
    #               site_id: identificador del cliente
    #               analysis_info: dict con los valores usados para el analisis
    #               queues: listado de colas que forman el backlog actual
    # output:
    #           event: evento generado
    ########################################################################
    def analyzeCaseManualBacklog(case, site_id, analysis_info, queues):
        log.info('Start:analyzeCaseManualBacklog')   
        try:
            event={}
            event["analysis_info"]=analysis_info
            event["analysis_info"]["analysis_date"]=datetime.now()

            event["case"]=case  
            try:
                event["queue"]=TableQueue.objects.get(objid=event["case"].case_currq2queue)    
            except  TableQueue.DoesNotExist: 
                event["queue"]=None      
           
            if (site_id):
                try:
                    event["site"]=Site.objects.get(site_id=site_id)
                except Site.DoesNotExist:
                    event["site"]=None
            else:
                try:
                    event["site"]=Site.objects.get(objid= event["case"].case_reporter2site)
                except Site.DoesNotExist:
                    event["site"]=None


            #Calculamos de nuevo los tags
            event['analysis_info']['tags'].extend(AnalysisCase.analyzeCommentsPatterns(event['case'].case_history))

            #Eliminamos duplicados
            event['analysis_info']['tags']=list(set(event['analysis_info']['tags']))


            if ( "site" in event and event["site"] and  event["site"].site_id):
                event.update( AnalysisAveria.analyzeSite({"site_id": event["site"].site_id}))    

         
            analysis_values=event['analysis_info']['analysis_details']
            if (analysis_values and ('type' in analysis_values) and (analysis_values['type']==Clasification.TYPE_CONTRACT_IN_PROGRESS)):
                event.update(AnalysisAveria.analyzeContract({"s_id":analysis_values['value']}))
            
            AnalysisAveria.evaluateAveria(event)
            AnalysisAveria.performAveria(event)

            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()                    
            queues=TableQueue.objects.filter(s_title__in=list(map(lambda x: x["queue"].upper(), queue_list))).all() 

            #Solo ponemos la averia en el ELK, si la cola del evento esta en el listado de colas que se le pasa al parametro
            #y tenemos informado datos del case 
            if ("case" in event and event["case"]) and (len(list(filter(lambda x: x.objid == event["case"].case_currq2queue, queues)))>0):
                Averia.setAveria(event)

            log.info('End:analyzeCaseManualBacklog')
            return event

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))


    ########################################################################
    # Metodo para analizar una averia de forma Manual, cuando no se encuentra
    # en el backlog actual del ELK
    #
    # input:
    #           params: parametros de entrada
    #               id_number - identificador de la averia (opcional)
    #               site_id - identificador del site (opcional)
    #               analysis_details - objeto a analizar
    # output:
    #           event: evento generado
    ########################################################################
    def analyzeCaseManualNotBacklog(params):
        
        log.info('Start:analyzeCaseManual')   
        RulesetAux.setFieldPatternValidator()
        
        if (not "analysis_details" in params):
            raise ApiException("Invalid parameters. analysis_details is required.")

        try:
            event=  {
                    "analysis_info": {
                                        "analysis_type":"Manual",
                                        "analysis_date":datetime.now(),
                                        "analysis_details": params["analysis_details"]
                                    }
                } 
            
            event["case"]=None
            event["queue"]=None
            event["site"]=None
            if ("id_number" in params):
                try:
                    event["case"]=TableCase.objects.get(id_number=params['id_number'])
                except TableCase.DoesNotExist:
                    event["case"]=None  

                if ("case" in event and event["case"]):
                    try:
                        event["queue"]=TableQueue.objects.get(objid=event["case"].case_currq2queue)    
                    except  TableQueue.DoesNotExist: 
                        event["queue"]=None
            
            if ("site_id" in params):
                try:
                    event["site"]=Site.objects.get(site_id= params["site_id"])
                except Site.DoesNotExist:
                    event["site"]=None

            elif ("case" in event and event["case"]):
                try:
                    event["site"]=Site.objects.get(objid= event["case"].case_reporter2site)
                except Site.DoesNotExist:
                    event["site"]=None
            

            if ("text" in params["analysis_details"]):
                 
                event['analysis_info']['analysis_details']
                tmpAnalysisObject=AnalysisCase.analyzeComments(text=params["analysis_details"]["text"], site=event["site"], comments=[])
                if (not tmpAnalysisObject):
                    event['analysis_info']['analysis_details']=params["analysis_details"]
                    event['analysis_info']['analysis_details']["date"]=datetime.now()
                    event['analysis_info']['analysis_details']["value"]=event['analysis_info']['analysis_details']["text"]
                else:
                    event['analysis_info']['analysis_details']=tmpAnalysisObject

                event['analysis_info']['analysis_details']['user']= params["request_user"]
                event['analysis_info']['tags']=AnalysisCase.analyzeCommentsPatterns( event['analysis_info']['analysis_details']['text'])
            elif ("case" in event and event["case"]):
                tmpAnalysis=AnalysisCase.analyzeComments(site=event['site'], comments=event['case'].getCommentsWorklog(), text=None)
                if (tmpAnalysis):
                    event['analysis_info']['analysis_details']=tmpAnalysis
                event['analysis_info']['analysis_details']['user']=  params["request_user"]
                event['analysis_info']['tags']=AnalysisCase.analyzeCommentsPatterns(event['case'].case_history)

            if ( "site" in event and event["site"] and  event["site"].site_id):
                event.update( AnalysisAveria.analyzeSite({"site_id": event["site"].site_id}))    

            analysis_values=event['analysis_info']['analysis_details']
            if (analysis_values and ('type' in analysis_values) and (analysis_values['type']==Clasification.TYPE_CONTRACT_IN_PROGRESS)):
                event.update(AnalysisAveria.analyzeContract({"s_id":analysis_values['value']}))

             
            AnalysisAveria.evaluateAveria(event)
            AnalysisAveria.performAveria(event)

            queue_list_param=Appparameter.objects.get(name__iexact='Queue analysis')
            queue_list=queue_list_param.getParamaterDataValue()                    
            queues=TableQueue.objects.filter(s_title__in=list(map(lambda x: x["queue"].upper(), queue_list))).all() 

            #Solo ponemos la averia en el ELK, si la cola del evento esta en el listado de colas que se le pasa al parametro
            #y tenemos informado datos del case 
            if ("case" in event and event["case"]) and (len(list(filter(lambda x: x.objid == event["case"].case_currq2queue, queues)))>0):
                Averia.setAveria(event)

            log.info('End:analyzeCaseManual')
            return event

        except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

    
    #####################################################################
    #   inputs:
    #       event: Objeto con el evento, que contiene toda la informacion
    #   output:
    #       return Devuelve alalisis final de la orden
    # 
    #####################################################################
    def evaluateAveria(event):
        log.info('Start: evaluateAveria')
        
        ruleset=Ruleset.objects.get(name="evaluate averia")
        rulesetImplementation=RulesetImplementation(ruleset)
        rulesetImplementation.executeRuleset(event)

        log.info('End: evaluateAveria')


    
    #####################################################################
    #   inputs:
    #       event: Objeto con el evento, que contiene toda la informacion
    #   output:
    #       return Devuelve alalisis final de la orden
    # 
    #####################################################################
    def performAveria(event):
        log.info('Start: performAveria')
        
        ruleset=Ruleset.objects.get(name="perform action averia")
        rulesetImplementation=RulesetImplementation(ruleset)
        rulesetImplementation.executeRuleset(event)

        log.info('End: performAveria')



class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self):
        super(PropagatingThread, self).join()
        if self.exc:
            log.error('Exception:'+type(self.exc).__name__ +" " +str(self.exc))
            raise self.exc
        return self.ret