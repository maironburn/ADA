from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Validationscript
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import ValidationscriptSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException
from .validators import ValidationScriptValidator
import importlib
import sys
import os
from django.conf import settings


log = logging.getLogger(__name__)

def getValidationscript(pk):
    return Validationscript.objects.get(pk=pk)


def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data


@api_view(["GET","POST"])
@permission_required('validationscript.view_validationscript','validationscript.add_validationscript', raise_exception=True)  
def validationscriptAction(request, format=None):
    if request.method=='GET':
        return listValidationscripts(request._request)
    elif request.method=='POST':
        return addValidationscript(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('validationscript.change_validationscript','validationscript.delete_validationscript', raise_exception=True)  
def modifyValidationscriptAction(request, pk, format=None):
    if request.method=='PUT':
        return updateValidationscript(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteValidationscript(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('validationscript.view_validationscript', raise_exception=True)  
# GET validationscript/
def listValidationscripts(request, format=None):
    try:
        log.info('Start:'+listValidationscripts.__name__)

        validationscript=Validationscript.objects.all()
        serializer = ValidationscriptSerializer(validationscript, many=True)

        log.info('End:'+listValidationscripts.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["PUT"])
@permission_required('validationscript.change_validationscript', raise_exception=True)  
# Put validationscript/1/
def updateValidationscript(request, pk, format=None):

    log.info('Start:'+updateValidationscript.__name__)
    try:
        validationscript=getValidationscript(pk)
    except Validationscript.DoesNotExist:
        return JsonResponse({ "error": { "message":"Condition not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)
    

        modifyCode=False
        if "code" in data:
            modifyCode=True
            ValidationScriptValidator.validateSyntaxCode(data["code"])
           
            #del data["code"]

        merged_data=getDataToUpdate(ValidationscriptSerializer(validationscript).data, data)
        ValidationScriptValidator.validateCode(data["code"], merged_data["classname"])

        serializer = ValidationscriptSerializer(instance=validationscript, data=merged_data)
        if serializer.is_valid():
            serializer.save()

            if (modifyCode):
                
                validationscript.setCode(merged_data["code"])

            log.info('End:'+updateValidationscript.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateValidationscript.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('validationscript.add_validationscript', raise_exception=True)  
# POST validationscript/
def addValidationscript(request, format=None):
   
    log.info('Start:'+addValidationscript.__name__)

    try:
        data = JSONParser().parse(request)

        if (not "code" in data):
            raise ApiException ("Code atribute is required")

        code=data["code"]
        ValidationScriptValidator.validateSyntaxCode(code)
        ValidationScriptValidator.validateCode(code, data["classname"])


        validationscript=Validationscript()
        serializer=ValidationscriptSerializer(validationscript, data=data)
        if serializer.is_valid():
            serializer.save()
            validationscript.setCode(code)  
            log.info('End:'+addValidationscript.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addValidationscript.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('validationscript.delete_validationscript', raise_exception=True)  
# DELETE validationscript/1/
def deleteValidationscript(request, pk, format=None):
    log.info('Start:'+deleteValidationscript.__name__)
    try:
        validationscript=getValidationscript(pk)
    except Validationscript.DoesNotExist:
        return JsonResponse({ "error": { "message":"Condition not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        validationscript.delete()
        log.info('End:'+deleteValidationscript.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["POST"])
@permission_required('validationscript.change_validationscript', raise_exception=True)  
# Put validationscript/1/
def reorder(request, format=None):
    log.info('Start:'+reorder.__name__)
    try:
        data = JSONParser().parse(request)
        output=[]
        for item in data:
            if (not "id" in item):
               raise ApiException("Invalid parameters. Item without id property.")     
            if (not "order" in item):   
                raise ApiException("Invalid parameters. Item without order property.")     

        for item in data:
            try:
                validationscript=getValidationscript(item["id"])
                validationscript.order=item["order"]
                validationscript.save()
                serializer=ValidationscriptSerializer(validationscript)
                output.append(serializer.data)

            except Validationscript.DoesNotExist:
                pass
        
        log.info('End:'+reorder.__name__)
        return JsonResponse(output, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

