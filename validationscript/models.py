from django.db import models
import django.db.models.options as options
from django.conf import settings
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)
from core.exceptions.customexceptions import ApiException
import os
import importlib
import sys
import shutil
import datetime

# Create your models here.

class Validationscript(models.Model):

    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    belongto = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=False)
    status = models.BooleanField(default=False)
    classname = models.TextField(blank=True, null=True)
    code = ""


    def setCode(self, data):
        classNameItems=self.classname.split(".")

        try:
            filename=os.path.join(settings.VALIDATION_SCRIPTS_FOLDER[self.belongto], classNameItems[0]+".py")

            try:
                vFile = open(filename, 'r')
                shutil.copy2(filename,filename+"."+datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
            except Exception as e:
                pass

            f=open(filename,'w')
            f.write(data + '\n')
            f.close()
        except Exception as e:
            raise ApiException(str(e))

        class_name=settings.VALIDATION_SCRIPTS_PATH[self.belongto]+"."+self.classname
        class_script_info=class_name.split(".")            
        class_module=".".join(class_script_info[0:-1])
        if (class_module in sys.modules):
            importlib.reload(sys.modules[class_module])    
        else:
            exec("import "+class_module)

    def getCode(self):
        classNameItems=self.classname.split(".")

        try:
            filename=os.path.join(settings.VALIDATION_SCRIPTS_FOLDER[self.belongto], classNameItems[0]+".py")
            f=open(filename,'r')
            code=f.read()
            f.close()
        except Exception as e:
            raise ApiException(str(e))  

        return code         

    
    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
        unique_together = (('classname', 'belongto',),
                            ('name', 'belongto'))
