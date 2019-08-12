from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Classification
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException
from .serializers import ClassificationSerializer

log = logging.getLogger(__name__)

def getClassification(pk):
    return Classification.objects.get(id=pk)

@api_view(["GET","POST"])
@permission_required('classification.view_classification','classification.add_classification', raise_exception=True)  
def classificationAction(request, format=None):
    if request.method=='GET':
        return listClassifications(request._request)
    elif request.method=='POST':
        return addClassification(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('clasification.view_clasification', raise_exception=True)  
# GET averias_clasification/
def listClassifications(request, format=None):
    try:
        log.info('Start:'+listClassifications.__name__)

        classifications=Classification.objects.all()
        serializer = ClassificationSerializer(classifications, many=True)

        log.info('End:'+listClassifications.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)