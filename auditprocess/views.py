from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Auditprocess
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import AuditprocessSerializer
import traceback


log = logging.getLogger(__name__)

def getAuditprocess(pk):
    return Auditprocess.objects.get(pk=pk)


@api_view(["GET"])
@permission_required('auditprocess.view_auditprocess', raise_exception=True)  
# GET auditprocess/
def listAuditprocess(request, format=None):
    try:
        log.info('Start:'+listAuditprocess.__name__)

        auditprocess=Auditprocess.objects.all()
        serializer = AuditprocessSerializer(auditprocess, many=True)

        log.info('End:'+listAuditprocess.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('auditprocess.delete_auditprocess', raise_exception=True)  
# DELETE auditprocess/1/
def deleteAuditprocess(request, pk, format=None):

    log.info('Start:'+deleteAuditprocess.__name__)
    try:
        auditprocess=getAuditprocess(pk)
    except Auditprocess.DoesNotExist:
        return JsonResponse({ "error": { "message":"Auditprocess not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        
        auditprocess.delete()
        log.info('End:'+deleteAuditprocess.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

