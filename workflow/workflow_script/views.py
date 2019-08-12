from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import WorkflowScriptSerializer
from .models import Workflow_script
from rest_framework.parsers import JSONParser
from core.utils.search_model import SearchableModel
import traceback

log = logging.getLogger(__name__)

@api_view(["POST"])
@permission_required('workflow_script.view_workflow_script', raise_exception=True)  
# POST workflow_script/search/
def listWorkflowScript(request, format=None):
    try:
        log.info('Start:'+listWorkflowScript.__name__)

        data = JSONParser().parse(request)

        all_workflowscripts=SearchableModel.search(Workflow_script,data)

        authorized_workflowscripts=[] 
        for wfm in all_workflowscripts:
            if wfm.isAuthorized(request.user):
                authorized_workflowscripts.append(wfm)


        serializer=WorkflowScriptSerializer(authorized_workflowscripts, many=True)

        log.info('End:'+listWorkflowScript.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)     


