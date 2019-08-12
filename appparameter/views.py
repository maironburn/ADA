from rest_framework import status
from .serializers import AppparameterSerializer
from core.utils.search_model import SearchableModel
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Appparameter
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.parsers import JSONParser
import traceback


import time


log = logging.getLogger(__name__)

def getAppParameter(pk):
    return Appparameter.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    log.info('Start:'+getDataToUpdate.__name__)
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)

    log.info('End:'+getDataToUpdate.__name__)
    
    return merged_data


@api_view(["GET"])
@permission_required('appparameter.view_appparameter', raise_exception=True)  
# GET appparameter/
def listParameters(request, format=None):
    try:
        log.info('Start:'+listParameters.__name__)

        parameters = Appparameter.objects.all()
        serializer = AppparameterSerializer(parameters, many=True)

        log.info('End:'+listParameters.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)



@api_view(["PUT"])
@permission_required('appparameter.change_appparameter', raise_exception=True)  
# PUT appparameter/1/
def updateParameter(request, pk, format=None):
    
    log.info('Start:'+updateParameter.__name__)
    try:
        parameter=getAppParameter(pk)
    except Appparameter.DoesNotExist:
        return JsonResponse({ "error": { "message":"AppParameter not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        data['modified_by']=request.user.username

        merged_data=getDataToUpdate(AppparameterSerializer(parameter).data, data)

        serializer = AppparameterSerializer(parameter, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateParameter.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

        log.info('End:'+updateParameter.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('appparameter.view_appparameter', raise_exception=True)  
# POST appparameter/search/
def searchParameters(request, format=None):
    
    log.info('Start:'+searchParameters.__name__)

    try:
        data = JSONParser().parse(request)
        data["hidden"]=False
        resultado=SearchableModel.search(Appparameter,data)
        serializer=AppparameterSerializer(resultado, many=True)

        log.info('End:'+searchParameters.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)        

  



 