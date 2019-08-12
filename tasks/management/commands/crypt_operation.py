"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from core.utils.crypto import ADACrypto
import os
import shutil
import datetime

from ApiADA.loggers import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Operations to encrypt/decrypt files'

    def handle(self, *args, **options):
        

        operation=input("Select the operation to execute (D|E) (D-Decrypt file, E- encrypt file):")

        if (operation==None or ( operation.upper()!= 'D' and operation.upper() != 'E' )):
            print("Option not avaliable")
            exit(-1)
        elif (operation.upper()== 'E'):
            fileDecrypted=input("Enter the name of file that you want encrypt with the complete path. For example: /xxxx/xxx/file :")
            try:
                vFile = open(fileDecrypted, 'r')
            except Exception as e:
                print ('Error: '+str(e))
                exit(-1)

            fileEncrypted=input("Enter the name of file where store encrypt data with the complete path :")
            try:
                vFile = open(fileEncrypted, 'r')
                option=input("The file: "+ fileEncrypted + " already exists. Do you want to create a backup and override it? (Y|N):")
                if (option==None or ( option.upper()!= 'Y' and option.upper() != 'N' )): 
                    print("Option not avaliable")
                    exit(-1)
                elif (option.upper()=='Y'):
                    shutil.copy2(fileEncrypted,fileEncrypted+"."+datetime.datetime.today().strftime('%Y%m%d'))
                elif (option.upper()=='N'):
                    pass
            except Exception as e:
                pass

            ADACrypto.encrypt_file(fileDecrypted, fileEncrypted)

            option=input("Do you want to delete original file ("+fileDecrypted+") ? (Y|N):")
            if (option != None and option.upper()== 'Y'):
                os.remove(fileDecrypted)
                print ("File:" +fileDecrypted+" deleted.")
            exit(0)


        elif (operation.upper()=='D'):
            fileEncrypted=input("Enter the name of file encrypted with the complete path. For example: /xxxx/xxx/file :")
            try:
                vFile = open(fileEncrypted, 'r')
            except Exception as e:
                print ('Error: '+str(e))
                exit(-1)

            fileDecrypted=input("Enter the name of file where store the data read from encrypted file, with the complete path :")
            try:
                vFile = open(fileDecrypted, 'r')
                option=input("The file: "+ fileDecrypted + " already exists. Do you want to create a backup and override it? (Y|N):")
                if (option==None or ( option.upper()!= 'Y' and option.upper() != 'N' )): 
                    print("Option not avaliable")
                    exit(-1)
                elif (option.upper()=='Y'):
                    shutil.copy2(fileDecrypted,fileDecrypted+"."+datetime.datetime.today().strftime('%Y%m%d'))
                elif (option.upper()=='N'):
                    pass
            except Exception as e:
                pass

            ADACrypto.decrypt_file(fileEncrypted, fileDecrypted)
            exit(0)


