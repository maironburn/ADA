from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Analysiserror
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import AnalysiserrorSerializer
import traceback

log = logging.getLogger(__name__)

def getAnalysisError(pk):
    return Analysiserror.objects.get(pk=pk)

@api_view(["GET"])
@permission_required('analysiserror.view_analysiserror', raise_exception=True)  
# GET analysiserror/
def listAnalysiserror(request, format=None):
    try:
        log.info('Start:'+listAnalysiserror.__name__)

        analysiserror=Analysiserror.objects.all()
        serializer = AnalysiserrorSerializer(analysiserror, many=True)

        log.info('End:'+listAnalysiserror.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('analysiserror.delete_analysiserror', raise_exception=True)  
# DELETE analysiserror/1/
def deleteAnalysiserror(request, pk, format=None):
    log.info('Start:'+deleteAnalysiserror.__name__)
    try:
        analysiserror=getAnalysisError(pk)
    except Analysiserror.DoesNotExist:
        return JsonResponse({ "error": { "message":"analysiserror not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        analysiserror.delete()
        log.info('End:'+deleteAnalysiserror.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

