from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from django.http import JsonResponse
import json
import traceback
from django.conf import settings
from ApiADA.loggers import logging
from rest_framework.permissions import AllowAny
from rest_framework.decorators import authentication_classes, permission_classes, api_view

log = logging.getLogger(__name__)

# Create your views here.


@api_view(["GET"])
@permission_classes((AllowAny,))  
def changeAppLogLevel(request, format=None):
    try:
        log_level=logging._checkLevel(request.GET['level'].upper())
        logging.getLogger().setLevel(log_level)
        jsonOutput=[]
        for handler in logging.getLogger().handlers:
            jsonOutput.append({'message':'Initial Handler:' + handler.name + " Level:" + logging.getLevelName(handler.level)})
            handler.setLevel(log_level)   
            jsonOutput.append({'message':'Final Handler:' + handler.name + " Level:" +logging.getLevelName(handler.level)})
        return JsonResponse(jsonOutput, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


