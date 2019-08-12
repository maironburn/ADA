from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Clasification
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import ClasificationSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

def getClasification(pk):
    return Clasification.objects.get(id=pk, editable=True)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

@api_view(["GET","POST"])
@permission_required('clasification.view_clasification','clasification.add_clasification', raise_exception=True)  
def clasificationAction(request, format=None):
    if request.method=='GET':
        return listClasifications(request._request)
    elif request.method=='POST':
        return addClasification(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('clasification.change_clasification','clasification.delete_clasification', raise_exception=True)  
def modifyClasificationAction(request, pk, format=None):
    if request.method=='PUT':
        return updateClasification(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteClasification(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('clasification.view_clasification', raise_exception=True)  
# GET averias_clasification/
def listClasifications(request, format=None):
    try:
        log.info('Start:'+listClasifications.__name__)

        clasifications=Clasification.objects.all()
        serializer = ClasificationSerializer(clasifications, many=True)

        log.info('End:'+listClasifications.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["PUT"])
@permission_required('clasification.change_clasification', raise_exception=True)  
# Put averias_clasification/1/
def updateClasification(request, pk, format=None):

    log.info('Start:'+updateClasification.__name__)
    try:
        clasification=getClasification(pk)
    except Clasification.DoesNotExist:
        return JsonResponse({ "error": { "message":"Item not found or not editable"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        merged_data=getDataToUpdate(ClasificationSerializer(clasification).data, data)

        serializer = ClasificationSerializer(clasification, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateClasification.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateClasification.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('clasification.add_clasification', raise_exception=True)  
# POST averias_clasification/
def addClasification(request, format=None):
   
    log.info('Start:'+addClasification.__name__)

    try:
        data = JSONParser().parse(request)

        clasification=Clasification()
        serializer=ClasificationSerializer(clasification, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addClasification.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addClasification.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('clasification.delete_clasification', raise_exception=True)  
# DELETE averias_clasification/1/
def deleteClasification(request, pk, format=None):
    log.info('Start:'+deleteClasification.__name__)
    try:
        clasification=getClasification(pk)
    except Clasification.DoesNotExist:
        return JsonResponse({ "error": { "message":"Item not found or not editable"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        clasification.delete()
        log.info('End:'+deleteClasification.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

