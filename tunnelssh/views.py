from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Tunnelssh
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import TunnelSSHSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

def getTunnelSSH(pk):
    return Tunnelssh.objects.get(id=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

@api_view(["GET","POST"])
@permission_required('tunnelssh.view_tunnelssh','tunnelssh.add_tunnelssh', raise_exception=True)  
def actionTunnelSSH(request, format=None):
    if request.method=='GET':
        return listTunnelSSH(request._request)
    elif request.method=='POST':
        return addTunnelSSH(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('tunnelssh.change_tunnelssh','tunnelssh.delete_tunnelssh', raise_exception=True)  
def modifyTunnelSSH(request, pk, format=None):
    if request.method=='PUT':
        return updateTunnelSSH(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteTunnelSSH(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('tunnelssh.view_tunnelssh', raise_exception=True)  
# GET tunnelssh/
def listTunnelSSH(request, format=None):
    try:
        log.info('Start:'+listTunnelSSH.__name__)

        tunnelsshs=Tunnelssh.objects.all()
        serializer = TunnelSSHSerializer(tunnelsshs, many=True)

        log.info('End:'+listTunnelSSH.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["PUT"])
@permission_required('tunnelssh.change_tunnelssh', raise_exception=True)  
# Put tunnelssh/1/
def updateTunnelSSH(request, pk, format=None):

    log.info('Start:'+updateTunnelSSH.__name__)
    try:
        tunnel=getTunnelSSH(pk)
    except Tunnelssh.DoesNotExist:
        return JsonResponse({ "error": { "message":"Tunnel not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        #merged_data=getDataToUpdate(TunnelSSHSerializer(tunnel).data, data)

        serializer = TunnelSSHSerializer(tunnel, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateTunnelSSH.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateTunnelSSH.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('tunnelssh.add_tunnelssh', raise_exception=True)  
# POST tunnelssh/
def addTunnelSSH(request, format=None):
   
    log.info('Start:'+addTunnelSSH.__name__)

    try:
        data = JSONParser().parse(request)

        tunnel=Tunnelssh()
        serializer=TunnelSSHSerializer(tunnel, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addTunnelSSH.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addTunnelSSH.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["DELETE"])
@permission_required('tunnelssh.delete_tunnelssh', raise_exception=True)  
# DELETE tunnelssh/1/
def deleteTunnelSSH(request, pk, format=None):
    log.info('Start:'+deleteTunnelSSH.__name__)
    try:
        tunnel=getTunnelSSH(pk)
    except Tunnelssh.DoesNotExist:
        return JsonResponse({ "error": { "message":"Tunnel not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        tunnel.delete()
        log.info('End:'+deleteTunnelSSH.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('tunnelssh.execute_tunnelssh', raise_exception=True)  
# POST tunnelssh/1/execute
def executeTunnelSSH(request, pk, format=None):
    log.info('Start:'+executeTunnelSSH.__name__)
    try:
        tunnel=getTunnelSSH(pk)
    except Tunnelssh.DoesNotExist:
        return JsonResponse({ "error": { "message":"Tunnel not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)
        if (data["action"]=='Connect'):
            tunnel.openTunnel()
        elif  (data["action"]=='Disconnect'):
            tunnel.closeTunnel()

        serializer = TunnelSSHSerializer(tunnel, many=False)    
        log.info('End:'+executeTunnelSSH.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

