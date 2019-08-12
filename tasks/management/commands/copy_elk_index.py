from django.core.management.base import BaseCommand
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery
import  json



class Command(BaseCommand):
    help = 'Copy data from one index to another one'

    def handle(self, *args, **options):
        migration_info_file=input("Input the path of file with the info to migrate:")

        try:
            with open( migration_info_file) as json_file:  
                migration_info = json.load(json_file)
        except Exception as e:
            print("Unable to open file: %s Error:%s" % (migration_info_file,str(e)))
            exit(-1)    

        if (not "source" in migration_info or (not(migration_info["source"]))):
            print("Source info is mandatory")   
            exit(-1)  
        
        if (not "target" in migration_info or (not(migration_info["target"]))):
            print("Target info is mandatory")    
            exit(-1) 

        if (not "server" in migration_info["source"] or (not (migration_info["source"]["server"]))):
            print("Source server info is mandatory")    
            exit(-1) 

        if (not "server" in migration_info["target"] or (not (migration_info["target"]["server"]))):
            print("Target server info is mandatory")    
            exit(-1)    

        if (not "port" in migration_info["source"] or (not (migration_info["source"]["port"]))):
            print("Source port info is mandatory")    
            exit(-1) 

        if (not "port" in migration_info["source"] or (not (migration_info["target"]["port"]))):
            print("Target port info is mandatory")    
            exit(-1)        

        if (not "index" in migration_info["source"] or (not (migration_info["source"]["index"]))):
            print("Source index info is mandatory")    
            exit(-1)    
        
        if (not "index" in migration_info["source"] or (not (migration_info["target"]["index"]))):
            print("Target index info is mandatory")    
            exit(-1)             

        if (not "certPem" in migration_info["source"] or (not (migration_info["source"]["certPem"]))):
            print("Source certPem info is mandatory")    
            exit(-1)   

        if (not "certPem" in migration_info["source"] or (not (migration_info["target"]["certPem"]))):
            print("Target certPem info is mandatory")    
            exit(-1)   

        if (not "certKey" in migration_info["source"] or (not (migration_info["source"]["certKey"]))):
            print("Source certKey info is mandatory")    
            exit(-1)    

        if (not "certKey" in migration_info["source"] or (not (migration_info["target"]["certKey"]))):
            print("Target certKey info is mandatory")    
            exit(-1)    

        if (not "certRootCa" in migration_info["source"] or (not (migration_info["source"]["certRootCa"]))):
            print("Source certRootCa info is mandatory")    
            exit(-1)    

        if (not "certRootCa" in migration_info["source"] or (not (migration_info["target"]["certRootCa"]))):
            print("Target certRootCa info is mandatory")    
            exit(-1)  

        if (not "sql" in migration_info["source"] or (not (migration_info["source"]["sql"]))):
            print("Source SQL info is mandatory")    
            exit(-1)    



        source_sql={
                    "action": "/"+migration_info["source"]["index"],
                    "body": migration_info["source"]["sql"]
                   }


        data_source=CustomElasticSearchQuery.executeSearchBaseDDL(sql=source_sql, 
                                                                  server=migration_info["source"]["server"], 
                                                                  port=migration_info["source"]["port"], 
                                                                  certPem=migration_info["source"]["certPem"], 
                                                                  certKey=migration_info["source"]["certKey"], 
                                                                  certRootCa=migration_info["source"]["certRootCa"], 
                                                                  onlySource=False)
        print("Documents to copy:"+str(len(data_source)))

        num_docs_copy=0
        for item in data_source:
            try:
                target_sql={
                            "protocol": "PUT",
                            "action": "/"+migration_info["target"]["index"]+"/"+item["_type"]+"/"+item["_id"],
                            "body": item["_source"]
                           } 
                
                CustomElasticSearchQuery.executeBaseDDL(sql=target_sql, 
                                                        server=migration_info["target"]["server"], 
                                                        port=migration_info["target"]["port"], 
                                                        certPem=migration_info["target"]["certPem"], 
                                                        certKey=migration_info["target"]["certKey"], 
                                                        certRootCa=migration_info["target"]["certRootCa"])
                num_docs_copy=num_docs_copy+1

            except Exception as e:
                print("Unable to copy document id:" + item["_id"] + " Error:"+str(e))
        
        print("Documents copied:"+str(num_docs_copy))
        exit(0)

      
