from django.core.exceptions import ValidationError
import json
from json_tricks import dumps
from core.exceptions.customexceptions import ApiException
import datetime, time
from django.conf import settings
import os
import re

class ValidationScriptValidator():

    def validateSyntaxCode(value):

        try:
            filename=os.path.join(settings.TMP_FOLDER, "tmp_"+str(time.mktime(datetime.datetime.now().timetuple()))+".py")
            f=open(filename,'w')
            f.write(value + '\n')
            f.close()
        except Exception as e:
            raise ApiException(str(e))
            
        try:    
            source = open(filename, 'r').read() + '\n'
            compile(source, filename, 'exec') 
        except Exception as e:
            raise ValidationError("code: Syntax Error. "+str(e))
        finally:
            os.remove(filename)    

        return True

    def validateCode(value, classname):
        strClassname=classname.split(".")[-1]

        #1. Verify the classname is equal to validationScript classname
        if (not re.search( 'class\s+'+strClassname+':', value)):
            raise ValidationError("code: The code should implement the class: "+strClassname)

        #2. Verify exists method validate
        if (not re.search( 'def\s+validate\s*\(', value)):
            raise ValidationError("code: The code should implement a validate method.")
        return True

