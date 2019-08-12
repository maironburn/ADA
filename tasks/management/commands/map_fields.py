"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.conf import settings
from django.core.management.base import BaseCommand
import os
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery

from ApiADA.loggers import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Operations to get fields of an index or a model'

    def handle(self, *args, **options):
        
        fields=[]

        operation=input("""Sources to get the fields:
                            1. Index of ElasticSearch
                            2. Model of application
                            Select the option (1:2):""")

        if (operation==None or ( operation.upper()!= '1' and operation.upper() != '2' )):
            print("Option not avaliable")
            exit(-1)
        elif (operation.upper()== '1'):
            index=input("Enter the name of elasticsearch index: ")
            type=input("Enter type of document in index %s: " % index)
            
            try:
                fields=self.getElasticsearchFields(index,type)

            except Exception as e:
                print ('Error: '+str(e))
                exit(-1)

        elif (operation.upper()=='2'):
            model=input("Enter the name of model,  for example: core.vodafone.smart.case.models.TableCase :")

            try:
                fields=self.getModelFields(model)

            except Exception as e:
                print ('Error: '+str(e))
                exit(-1)
        
        print ("Fields:")  
        print ("\n".join(fields))

    def getElasticsearchFields(self, index, type):
        fields=[]
        log.info('Start:getElasticsearchFields')

        sql=    {
                    "protocol": "GET",
                    "action": "/%s/%s/_mapping/field/*" % (index, type),
                    "body": 
                    {
                    }
                }
            
        fieldsInfo=CustomElasticSearchQuery.executeDDL(sql)
        if (fieldsInfo):
            for key, value in fieldsInfo[index]["mappings"][type].items():
                fields.append(key.replace(".","/"))

        fields.sort()

        log.info('End:getElasticsearchFields')

        return fields


    def getObjectMetaFields(prefix, data):
            if (prefix != ""):
                prefix=prefix + "/"	
            tmpOutput=[]
            for field in data._meta.fields:
                if field.is_relation:
                    tmpOutput.extend(Command.getObjectMetaFields(prefix+field.name, field.related_model))
                else:
                    tmpOutput.append(prefix+field.name)
            
            return tmpOutput

    def getModelFields(self, model):
        fields=[]
        log.info('Start:getModelFields')

        model_info=model.split(".")
        exec_class=model_info[-1]
        exec_package=".".join(model_info[0:-1])

       
        local_var_command={}
        
        import_command="from "+exec_package+ " import "+exec_class+"\n" 
        constructor_command="obj="+exec_class+"()\n"
       
        exec_command=import_command + constructor_command


        exec(exec_command,{}, local_var_command)
        obj=local_var_command["obj"]

        fields=[name for name in dir(obj.__class__) if isinstance(getattr(obj.__class__, name), property)]
        fields.extend(Command.getObjectMetaFields('',obj))        
        fields=list(set(fields))
        fields.sort()
            

        log.info('End:getModelFields')

        return fields
