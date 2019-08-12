from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializer import WorkflowmethodparameterSerializer
from .models import Workflow_method_parameter
from rest_framework.parsers import JSONParser
from core.utils.search_model import SearchableModel
import traceback

log = logging.getLogger(__name__)

@api_view(["POST"])
@permission_required('workflow_method_parameter.view_workflow_method_parameter', raise_exception=True)  
# POST workflow_method_parameter/search/
def listWorkflowMethodParameter(request, format=None):
    try:
        log.info('Start:'+listWorkflowMethodParameter.__name__)

        data = JSONParser().parse(request)

        all_workflowmethodparameters=SearchableModel.search(Workflow_method_parameter,data)

        authorized_workflowmethodparameters=[] 
        for wfm in all_workflowmethodparameters:
            if wfm.isAuthorized(request.user):
                authorized_workflowmethodparameters.append(wfm)


        serializer=WorkflowmethodparameterSerializer(authorized_workflowmethodparameters, many=True)

        log.info('End:'+listWorkflowMethodParameter.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)     


