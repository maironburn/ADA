from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from appparameter.models import Appparameter
from core.vodafone.smart.queue.models import TableQueue
from core.vodafone.smart.case.models import TableCase
from core.vodafone.smart.site.models import Site
from core.vodafone.smart.contract.models import Contract
from pattern.models import Pattern
import traceback
import json
import re
from json_tricks import dumps
from core.vodafone.smart import smart_query
from datetime import datetime
from clasification.models import Clasification

log = logging.getLogger(__name__)

class AnalysisCase:

   
    
    def analyzeComments(text, site, comments):

        site_id= site.site_id if site else ""
        log.info('Start:analyzeComments site: '+ site_id)
        


       

        analysis_order_param=Appparameter.objects.get(name__iexact='Analysis comments priority')
        analysis_order=analysis_order_param.getParamaterDataValue()
        analysis_order.sort(key=lambda x: x['order'], reverse=False)

           
        if (site):

            #siteOrders = Contract.objects.raw('SELECT co.objid, co.s_id FROM table_contract co, table_contr_schedule cs where cs.ship_to2site=%s and co.objid=cs.schedule2contract order by co.create_dt desc ', [site.objid])

            query_contract_site="""SELECT co.objid, co.s_id 
                                FROM table_contract co, table_contr_schedule cs
                                WHERE cs.ship_to2site=%s 
                                AND co.objid=cs.schedule2contract order by co.create_dt desc """  % (site.objid)

            siteOrders=smart_query.my_custom_sql('smart_gg', query_contract_site)

        else:
            siteOrders=[]
            
        output=None

        if (text):
            for an in analysis_order:
                if (an['analysis']=='orders'):
                     output=AnalysisCase.analyzeCommentsOrders(siteOrders,text, datetime.now())
                elif (an['analysis']=='exceptions'):
                     output=AnalysisCase.analyzeCommentsExceptions(text, datetime.now())             
                
                if (output):
                    break 

        #Analyze the comments to search java exception, order or pattern
        for comment in reversed(comments):
            # Si ya hemos encontrado una coincidencia, no recorremos mas comentarios    
            if (output):
                break  
            
            for an in analysis_order:
                if (an['analysis']=='orders'):
                     output=AnalysisCase.analyzeCommentsOrders(siteOrders,comment['text'], comment['date'])
                elif (an['analysis']=='exceptions'):
                     output=AnalysisCase.analyzeCommentsExceptions(comment['text'], comment['date'])             
                
                if (output):
                    break  
 


        log.info('End:analyzeComments: output: ' + str(output) )
        return output

    def analyzeCommentsOrders(siteOrders, text, date):
        output=None
        for order in siteOrders:
            if order["s_id"] in text:
                output={}
                output["type"]=Clasification.TYPE_CONTRACT_IN_PROGRESS
                output["value"]=order["s_id"]
                output["date"]=date
                output["text"]=text
                break
        
        return output
        

    def analyzeCommentsExceptions(text, date):

        output=None
        java_exception_regex=re.compile('(?:[a-zA-Z_$][a-zA-Z\d_$]*\.)*(?P<exception_class>[a-zA-Z_$][a-zA-Z\d_$]*Exception)(:?)(\s*)', re.I)

        existsJavaException=False    
        java_exception_class=None    
        java_exception_comments=''
        java_exception_backtrace=''
        for m in java_exception_regex.finditer(text):
            existsJavaException=True
            java_exception_info=m
            java_exception_class=java_exception_info.group('exception_class')
            temp_txt=text[java_exception_info.end():]
            lines=temp_txt.split("\n")
            

            java_exception_comments=''
            java_exception_backtrace=''
            isComment=True
            for line in lines:
                line_without_tabs=line.replace('\t','').strip()
                isBacktrace=line_without_tabs.startswith( 'at' )  
                if (isComment):
                    if (isBacktrace):
                        isComment=False
                        if (not "(Unknown Source)" in line_without_tabs):
                            java_exception_backtrace=line_without_tabs
                            break
                    elif line_without_tabs != '':
                        if java_exception_comments.find('</') >= 0 :
                                java_exception_comments=java_exception_comments[ :java_exception_comments.find('</')]
                                isComment=False
                        else:        
                            java_exception_comments += line_without_tabs
                    else:
                        isComment=False   
                else:
                    if (isBacktrace):
                        if (not "(Unknown Source)" in line_without_tabs):
                            java_exception_backtrace=line_without_tabs
                            break
                    else:
                        break    
                
            
            java_exception_comments=java_exception_comments.replace('An internal error has occurred.  Please contact your System Administrator.','')

            if (java_exception_class and len(java_exception_backtrace)>0):
                break

        if (existsJavaException):
            value=''
            if ( (len(java_exception_comments)==0) or (java_exception_comments=='null')):
                value=java_exception_backtrace.replace('at ','')
            else:
                value=java_exception_comments

            output={    "type":Clasification.TYPE_INTERNAL_ERROR, 
                        "date": date,
                        "value": java_exception_class +  "-" + value ,
                        "text": text
                    }
        

        return output

    def analyzeCommentsPatterns(text):

        output=[]
        patterns=Pattern.objects.filter(enable=True).order_by('priority')
        for pattern in patterns:
            pattern_regex=re.compile(pattern.pattern, re.I)            
            for m in pattern_regex.finditer(text):                
                if not pattern.label in output:
                    output.append(pattern.label)
        return output