from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
import traceback
import json
from core.vodafone.smart.site.models import Site
from core.validation.models import Validation
from validationscript.models import Validationscript
from django.conf import settings


log = logging.getLogger(__name__)


class AssetValidation:

    def validate(params):

        log.info('Start: validate')

        validation=Validation()

        if not "site_id" in params:
            raise ApiException("Invalid params. site_id required.")
        
        try:
            site=Site.objects.get(site_id=params["site_id"])
        except Site.DoesNotExist:
            validation.setValues(-1,"Site_id not found", "Site_id %s not found" % params["site_id"] )
        
        if (validation.code == 0 ):
            validationScripts=Validationscript.objects.filter(belongto='ASSET').filter(status=True).order_by('order').all()
            log.info("Number of scripts to validate:"+str(len(validationScripts)))
            for validationScript in validationScripts:
                if (validation.code == 0):
                     
                    try:

                        class_script_info=(settings.VALIDATION_SCRIPTS_PATH["ASSET"]+"."+validationScript.classname).split(".")
                        exec_method="validate"
                        exec_class=class_script_info[-1]
                        exec_package=".".join(class_script_info[0:-1])
                        
                        
                        local_var_command={"site": site}
                        import_command="from "+exec_package+ " import "+exec_class+"\n" 
                        method_command="validation="+exec_class+"."+exec_method+"(site)"
                        exec_command=import_command + method_command

                        log.info('Execute script  :'+validationScript.name)

                        exec(exec_command,{}, local_var_command)

                        validation=local_var_command["validation"]
                        
                    except  Exception as e:
                        log.error('Exception:'+type(e).__name__ +" " +str(e))
                        validation.setValues(-1,"Unable to execute validationScript", 'Unable to execute validationScript:'+validationScript.name)
                        

        log.info('End: validate')
        return validation
