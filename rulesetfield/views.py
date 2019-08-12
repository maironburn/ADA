from django.shortcuts import render
from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Rulesetfield
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import RulesetfieldSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException
from core.utils.search_model import SearchableModel


log = logging.getLogger(__name__)

def getRulesetfield(pk):
    return Rulesetfield.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data


@api_view(["GET","POST"])
@permission_required('rulesetfield.view_rulesetfield','rulesetfield.add_rutsetfield', raise_exception=True)  
def rulesetfieldAction(request, format=None):
    if request.method=='GET':
        return listRulesetfields(request._request)
    elif request.method=='POST':
        return addRulesetfield(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('rulesetfield.change_rulesetfield','rulesetfield.delete_rulesetfield', raise_exception=True)  
def modifyRulesetfieldAction(request, pk, format=None):
    if request.method=='PUT':
        return updateRulesetfield(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteRulesetfield(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('rulesetfield.view_rulesetfield', raise_exception=True)  
# GET rulesetfield/
def listRulesetfields(request, format=None):
    try:
        log.info('Start:'+listRulesetfields.__name__)

        rulesetfields=Rulesetfield.objects.all()
        serializer=RulesetfieldSerializer(rulesetfields, many=True)

        log.info('End:'+listRulesetfields.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["PUT"])
@permission_required('rulesetfield.change_rulesetfield', raise_exception=True)  
# Put rulesetfield/1/
def updateRulesetfield(request, pk, format=None):

    log.info('Start:'+updateRulesetfield.__name__)
    try:
        rulesetfield=getRulesetfield(pk)
    except rulesetfield.DoesNotExist:
        return JsonResponse({ "error": { "message":"Rulesetfield not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        merged_data=getDataToUpdate(ConditionSerializer(rulesetfield).data, data)

        serializer = ConditionSerializer(rulesetfield, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateRulesetfield.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateRulesetfield.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('rulesetfield.add_rulesetfield', raise_exception=True)  
# POST rulesetfield/
def addRulesetfield(request, format=None):
   
    log.info('Start:'+addRulesetfield.__name__)

    try:
        data = JSONParser().parse(request)

        rulesetfield=Rulesetfield()
        serializer=RulesetfieldSerializer(rulesetfield, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addRulesetfield.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addRulesetfield.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('rulesetfield.delete_rulesetfield', raise_exception=True)  
# DELETE rulesetfield/1/
def deleteRulesetfield(request, pk, format=None):
    log.info('Start:'+deleteRulesetfield.__name__)
    try:
        rulesetfield=getRulesetfield(pk)
    except rulesetfield.DoesNotExist:
        return JsonResponse({ "error": { "message":"Rulesetfield not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        rulesetfield.delete()
        log.info('End:'+deleteRulesetfield.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["POST"])
@permission_required('rulesetfield.view_rulesetfield', raise_exception=True)  
# POST rulesetfield/search/
def searchRulesetfield(request, format=None):
    
    log.info('Start:'+searchRulesetfield.__name__)

    try:
        data = JSONParser().parse(request)
        resultado=SearchableModel.search(Rulesetfield,data)
        serializer=RulesetfieldSerializer(resultado, many=True)

        log.info('End:'+searchRulesetfield.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)        