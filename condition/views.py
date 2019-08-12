from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Condition
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import ConditionSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

def getCondition(pk):
    return Condition.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

@api_view(["GET","POST"])
@permission_required('condition.view_condition','condition.add_condition', raise_exception=True)  
def conditionAction(request, format=None):
    if request.method=='GET':
        return listConditions(request._request)
    elif request.method=='POST':
        return addCondition(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('condition.change_condition','condition.delete_condition', raise_exception=True)  
def modifyConditionAction(request, pk, format=None):
    if request.method=='PUT':
        return updateCondition(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteCondition(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('condition.view_condition', raise_exception=True)  
# GET condition/
def listConditions(request, format=None):
    try:
        log.info('Start:'+listConditions.__name__)

        conditions=Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)

        log.info('End:'+listConditions.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["PUT"])
@permission_required('condition.change_condition', raise_exception=True)  
# Put condition/1/
def updateCondition(request, pk, format=None):

    log.info('Start:'+updateCondition.__name__)
    try:
        condition=getCondition(pk)
    except Condition.DoesNotExist:
        return JsonResponse({ "error": { "message":"Condition not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        merged_data=getDataToUpdate(ConditionSerializer(condition).data, data)

        serializer = ConditionSerializer(condition, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateCondition.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateCondition.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('condition.add_condition', raise_exception=True)  
# POST condition/
def addCondition(request, format=None):
   
    log.info('Start:'+addCondition.__name__)

    try:
        data = JSONParser().parse(request)

        condition=Condition()
        serializer=ConditionSerializer(condition, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addCondition.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addCondition.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('condition.delete_condition', raise_exception=True)  
# DELETE condition/1/
def deleteCondition(request, pk, format=None):
    log.info('Start:'+deletePattern.__name__)
    try:
        condition=getCondition(pk)
    except Condition.DoesNotExist:
        return JsonResponse({ "error": { "message":"Condition not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        condition.delete()
        log.info('End:'+deletePattern.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

