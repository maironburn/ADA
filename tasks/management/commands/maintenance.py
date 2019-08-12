"""
Compress and delete files 
Create permissions (read only) to models for a set of groups
"""
from django.core.management.base import BaseCommand
from ApiADA.constantes import Constantes
from appparameter.models import Appparameter
from datetime import timedelta, datetime
from django.conf import settings
from auditprocess.models import Auditprocess
from analysiserror.models import Analysiserror
import os
import shutil
import datetime
import glob
import time
import gzip


from ApiADA.loggers import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Operations to maintenance logs files and some tables of BBDD (analysis_error_analysis_error, auditprocess_auditprocess)'

    def handle(self, *args, **options):

        self.maintenanceFiles()
        self.maintenanceTableAnalysis()
        self.maintenanceTableAnalysisError()
        

    def maintenanceFiles(self):
        configurations=[]
        configurations_file=open(os.path.join(settings.CONFIG_DIR, 'maintenance.cfg'),'r')
        row=0
        for configuration in configurations_file:
            row=row+1
            if (not configuration.startswith('#')) and (configuration.strip()!=""):                
                try:
                    configuration_fields=configuration.split("|")
                    if configuration_fields[0].strip()=="" or configuration_fields[1].strip()=="":
                        raise Exception('Invalid configuration')

                    configurations.append({ "folder": configuration_fields[0].strip(),
                                            "pattern": configuration_fields[1].strip(),
                                            "days_zip": int(configuration_fields[2].strip()),
                                            "days_delete": int(configuration_fields[3].strip())
                                        })
                    
                except Exception:
                    print('Invalid configuration in file: '+os.path.join(settings.CONFIG_DIR, 'maintenance.cfg')+ ' row:'+ str(row) + ' content:'+ configuration)

        configurations_file.close()

      
        for configuration in configurations:
            folders=[]
            for dirpath, dirnames, files in os.walk(configuration["folder"]):            
                if not os.path.join(dirpath) in folders:
                    self.manageFolder(dirpath,configuration)
                    folders.append(os.path.join(dirpath))

                for folder in dirnames:
                    if not os.path.join(dirpath,folder) in folders:
                        self.manageFolder(os.path.join(dirpath,folder),configuration)
                        folders.append(os.path.join(dirpath,folder))
    

    def maintenanceTableAnalysis(self):
        
        daysDelAuditprocess_list_param=Appparameter.objects.get(name__iexact='Days of Auditprocess table')
        daysDelAnalysisError=daysDelAuditprocess_list_param.getParamaterDataValue()

        try:
            dateToDel=(datetime.datetime.now() - datetime.timedelta(days=daysDelAnalysisError))
            Auditprocess.objects.filter(start_date__lte=dateToDel).delete()

        except Exception as e:
           print ('Error to try delete records of auditprocess_auditprocess table of sqlite')  


    def maintenanceTableAnalysisError(self):
        
        daysDelAnalysisError_list_param=Appparameter.objects.get(name__iexact='Days of Analysiserror table')
        daysDelAnalysisError=daysDelAnalysisError_list_param.getParamaterDataValue()

        try:
            dateToDel=(datetime.datetime.now() - datetime.timedelta(days=daysDelAnalysisError))
            Analysiserror.objects.filter(modified_date__lte=dateToDel).delete()

        except Exception as e:
            print ('Error to try delete records of analysiserror_analysiserror table of sqlite')  

    def manageFolder(self, folder, configuration):
        print('Manage folder:'+folder)     
        os.chdir(folder)    
        files=[]
        for file in glob.glob(configuration["pattern"]):
            files.append(file)
        for file in glob.glob(configuration["pattern"]+".gz"):
            files.append(file)
            
        for file in files:
            self.manageFile(os.path.join(folder, file),configuration) 
           


    def manageFile(self, file, configuration):
        print('Manage file:'+file)     
        now = time.time()
        if os.stat(file).st_mtime <= now - configuration["days_delete"] * 24 * 60 * 60:
            self.deleteFile(file)
        elif os.stat(file).st_mtime <= now - configuration["days_zip"] * 24 * 60 * 60:
            self.zipFile(file)
        else:
            pass


    def zipFile(self, file):
        print('Zip file:'+file)     
        targetFileCompress=file+".gz"
        modifiedTimeOrigin=os.stat(file).st_mtime
        accessTimeOrigin=os.stat(file).st_atime
        try:
            if not file.endswith('.gz'):

                with open(file, 'rb') as f_in, gzip.open(targetFileCompress, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

                os.utime(targetFileCompress, (modifiedTimeOrigin, modifiedTimeOrigin))
                os.remove(file)

        except Exception as e:
            print ('Error to try compress the file: ' + file) 

    def deleteFile(self, file):
        print('Delte file:'+file) 
        try:
            os.remove(file)

        except Exception as e:
            print ('Error to try delete the file: ' + file)
