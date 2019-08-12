from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Workflow
from django.contrib.auth.models import Group
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import WorkflowSerializer
import traceback


log = logging.getLogger(__name__)



@api_view(["GET"])
@permission_required('workflow.view_workflow', raise_exception=True)  
# GET workflow/authorized/
def listWorkflowAuthorized(request, format=None):
    try:
        log.info('Start:'+listWorkflowAuthorized.__name__)

        workflows=Workflow.objects.filter(groups__in=request.user.groups.all()).distinct()
        serializer = WorkflowSerializer(workflows, many=True)

        log.info('End:'+listWorkflowAuthorized.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)
