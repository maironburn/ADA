from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Action
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import ActionSerializer
from rest_framework.parsers import JSONParser
from core.utils.search_model import SearchableModel
from core.exceptions.customexceptions import ApiException
import traceback

log = logging.getLogger(__name__)

def getAction(pk):
    return Action.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data


@api_view(["GET","POST"])
@permission_required('action.view_action','action.add_action', raise_exception=True)  
def actionAction(request, format=None):
    if request.method=='GET':
        return listActions(request._request)
    elif request.method=='POST':
        return addAction(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('action.change_action','action.delete_action', raise_exception=True)  
def modifyAction(request, pk, format=None):
    if request.method=='PUT':
        return updateAction(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteAction(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["GET"])
@permission_required('action.view_action', raise_exception=True)  
# GET action/
def listActions(request, format=None):
    try:
        log.info('Start:'+listActions.__name__)

        actions=Action.objects.all()
        serializer = ActionSerializer(actions, many=True)

        log.info('End:'+listActions.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["POST"])
@permission_required('action.view_action', raise_exception=True) 
# POST action/search/
def searchActions(request, format=None):
    log.info('Start:'+searchActions.__name__)

    try:
        data = JSONParser().parse(request)
        resultado=SearchableModel.search(Action,data)
        serializer=ActionSerializer(resultado, many=True)

        log.info('End:'+searchActions.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message": str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT"])
@permission_required('action.change_action', raise_exception=True)  
# Put action/1/
def updateAction(request, pk, format=None):

    log.info('Start:'+updateAction.__name__)
    try:
        action=getAction(pk)
    except Action.DoesNotExist:
        return JsonResponse({ "error": { "message":"Action not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        # merged_data=getDataToUpdate(ActionSerializer(action).data, data)
        merged_data=data

        serializer = ActionSerializer(action, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateAction.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateAction.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('action.add_action', raise_exception=True)  
# POST action/
def addAction(request, format=None):
   
    log.info('Start:'+addAction.__name__)

    try:
        data = JSONParser().parse(request)

        action=Action()
        serializer=ActionSerializer(action, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addAction.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addAction.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('action.delete_action', raise_exception=True)  
# DELETE action/1/
def deleteAction(request, pk, format=None):
    log.info('Start:'+deleteAction.__name__)
    try:
        action=getAction(pk)
    except Action.DoesNotExist:
        return JsonResponse({ "error": { "message":"Action not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        action.delete()
        log.info('End:'+deleteAction.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)



