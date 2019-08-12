from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.parsers import JSONParser
from .models import Pattern
from .serializers import PatternSerializer
import traceback
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

def getPattern(pk):
    return Pattern.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

@api_view(["GET","POST"])
@permission_required('pattern.view_pattern','pattern.add_pattern', raise_exception=True)  
def patternAction(request, format=None):
    if request.method=='GET':
        return listPattern(request._request)
    elif request.method=='POST':
        return addPattern(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('pattern.change_pattern','pattern.delete_pattern', raise_exception=True)  
def modifyAction(request, pk, format=None):
    if request.method=='PUT':
        return updatePattern(request._request, pk=pk)
    elif request.method=='DELETE':
        return deletePattern(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["GET"])
@permission_required('pattern.view_pattern', raise_exception=True)  
# GET pattern/
def listPattern(request, format=None):
    try:
        log.info('Start:'+listPattern.__name__)

        patterns = Pattern.objects.all()
        serializer = PatternSerializer(patterns, many=True)

        log.info('End:'+listPattern.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)



@api_view(["PUT"])
@permission_required('pattern.change_pattern', raise_exception=True)  
# PUT pattern/1/
def updatePattern(request, pk, format=None):
    
    log.info('Start:'+updatePattern.__name__)
    try:
        pattern=getPattern(pk)
    except Pattern.DoesNotExist:
        return JsonResponse({ "error": { "message":"Pattern not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        merged_data=getDataToUpdate(PatternSerializer(pattern).data, data)

        serializer = PatternSerializer(pattern, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updatePattern.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updatePattern.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('pattern.add_pattern', raise_exception=True)  
# POST pattern/
def addPattern(request, format=None):
    
    log.info('Start:'+addPattern.__name__)

    try:
        data = JSONParser().parse(request)

        pattern=Pattern()
        serializer=PatternSerializer(pattern, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addPattern.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addPattern.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)        


@api_view(["DELETE"])
@permission_required('pattern.delete_pattern', raise_exception=True)  
# DELETE pattern/1/
def deletePattern(request, pk, format=None):
    
    log.info('Start:'+deletePattern.__name__)
    try:
        pattern=getPattern(pk)
    except Pattern.DoesNotExist:
        return JsonResponse({ "error": { "message":"Pattern not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        pattern.delete()
        log.info('End:'+deletePattern.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)



 