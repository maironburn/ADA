from django.shortcuts import render


from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import WorkflowmethodSerializer
from .models import Workflow_method
from workflow.workflow_method.workflow_method_parameter.models import Workflow_method_parameter
from rest_framework.parsers import JSONParser
from core.utils.search_model import SearchableModel
from core.exceptions.customexceptions import ApiException
import traceback
import json
import os
#import requests
from django.conf import settings

log = logging.getLogger(__name__)

@api_view(["GET"])
@permission_required('workflow_method.view_workflow_method', raise_exception=True)  
# GET workflow_method/
def listWorkflowMethod(request, format=None):
    try:
        log.info('Start:'+listWorkflowMethod.__name__)

        all_workflowmethods=Workflow_method.objects.all()

        authorized_workflowmethods=[] 
        for wfm in all_workflowmethods:
            if wfm.isAuthorized(request.user):
                authorized_workflowmethods.append(wfm)


        serializer=WorkflowmethodSerializer(authorized_workflowmethods, many=True)

        log.info('End:'+listWorkflowMethod.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)     


@api_view(["POST"])
@permission_required('workflow_method.execute_workflow_method', raise_exception=True) 
# POST workflow_method/1/execute/
def execute(request, pk, format=None):

    #prueba
    #result=requests.get('https://localhost:9200/_cat/indices?v', cert=(os.path.join(settings.CERTS_FOLDER,'kirk.pem'),os.path.join(settings.CERTS_FOLDER,'kirk-key.pem') ), verify=os.path.join(settings.CERTS_FOLDER,'root-ca.pem'))
    #prueba


    isAllowed=False
    try:
        log.info('Start:'+execute.__name__)

        workflow_method=Workflow_method.objects.get(id=pk)
        isAllowed=workflow_method.isAuthorized(request.user)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)     

    if not isAllowed:
            raise PermissionDenied
    
    try:

        param_definitions=Workflow_method_parameter.objects.filter(workflow_method=workflow_method.id).all()
        param_definitions_names=list(map(lambda p: p.name, param_definitions))
        param_values = JSONParser().parse(request)

        for param in param_values:
            if param in param_definitions_names:
                pass
            else:
                raise ApiException('Parameter: '+ param + ' no allowed for this method.')

        for param in param_definitions:
            if (param.optional):
                pass
            else:     
                if (param.name in param_values):
                    pass
                else:
                    raise ApiException('Parameter: '+ param.name + ' not informed in request.')

        param_values["request_user"]=request.user.username
        try:

            class_method_info=workflow_method.class_method.split(".")
            exec_method=class_method_info[-1]
            exec_class=class_method_info[-2]
            exec_package=".".join(class_method_info[0:-2])
            
            local_var_command={}
            import_command="from "+exec_package+ " import "+exec_class+"\n" 
            method_command="outputWF="+exec_class+"."+exec_method+"("+json.dumps(param_values)+")"
            exec_command=import_command + method_command
            
        except  Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            raise ApiException('Unable to setup the workflow execute command.') 
            
            
        exec(exec_command,{}, local_var_command)

        try:

            serializer_method_info=workflow_method.serializer_method.split(".")
            serializer_class=serializer_method_info[-1]
            serializer_package=".".join(serializer_method_info[0:-1])

            #local_var_serializer_command={}
            import_command="from "+serializer_package+ " import "+serializer_class+"\n" 
            method_command="if outputWF.__class__.__name__ == 'list':\n"
            method_command+="    serializer="+serializer_class+ "(data=outputWF, many=True)\n"
            method_command+="else:\n"    
            method_command+="    serializer="+serializer_class+ "(data=outputWF)\n"    
            additional_command="serializer.is_valid()"
            exec_command=import_command + method_command + additional_command

        except  Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            raise ApiException('Unable to setup the workflow serializer command.') 

        exec(exec_command,{}, local_var_command)

        log.info('End:'+execute.__name__)
        return JsonResponse(local_var_command['serializer'].validated_data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)     
    
@api_view(["POST"])
@permission_required('workflow_method.view_workflow_method', raise_exception=True)  
# POST workflow_method/search/
def searchWorkflowMethod(request, format=None):
    try:
        log.info('Start:'+listWorkflowMethod.__name__)

        data = JSONParser().parse(request)

        all_workflowmethods=SearchableModel.search(Workflow_method,data)

        authorized_workflowmethods=[] 
        for wfm in all_workflowmethods:
            if wfm.isAuthorized(request.user):
                authorized_workflowmethods.append(wfm)


        serializer=WorkflowmethodSerializer(authorized_workflowmethods, many=True)

        log.info('End:'+listWorkflowMethod.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)