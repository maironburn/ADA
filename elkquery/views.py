from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Elkquery
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import ElkquerySerializer
import traceback
import json
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException
from django.conf import settings
from core.elasticsearch.elasticsearch_query import CustomElasticSearchQuery

from .models import Group

log = logging.getLogger(__name__)

def getElasticsearchQuery(pk, groups):
    return Elkquery.objects.get(pk=pk, group__in=groups)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

def getUserGroup(groups):
    tmpGroups=[]
    
    for group in groups:
        priority=settings.GROUPS_PRIORITY[group.name]
        tmpGroups.append({ "id": group.id, "name": group.name ,"priority": priority})
    
    tmpGroups.sort(key=lambda x: x["priority"])
    if (len(tmpGroups)>0):
        return tmpGroups[0]
    else:
        raise ApiException('Unable to get group from user.')    

    

@api_view(["GET","POST"])
@permission_required('elkquery.view_elkquery','elkquery.add_elkquery', raise_exception=True)  
def elasticsearchqueryAction(request, format=None):
    if request.method=='GET':
        return listElasticsearchquerys(request._request)
    elif request.method=='POST':
        return addElasticsearchquery(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('elkquery.change_elkquery','elkquery.delete_elkquery', raise_exception=True)  
def modifyElasticsearchqueryAction(request, pk, format=None):
    if request.method=='PUT':
        return updateElasticsearchquery(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteElasticsearchquery(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('elkquery.view_elkquery', raise_exception=True)  
# GET elasticsearch_query/
def listElasticsearchquerys(request, format=None):
    try:
        log.info('Start:'+listElasticsearchquerys.__name__)
        queries=Elkquery.objects.filter(group__in=request.user.groups.all())
        serializer = ElkquerySerializer(queries, many=True)

        log.info('End:'+listElasticsearchquerys.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT"])
@permission_required('elkquery.change_elkquery', raise_exception=True)  
# Put elasticsearch_query/1/
def updateElasticsearchquery(request, pk, format=None):

    log.info('Start:'+updateElasticsearchquery.__name__)
    try:
        query=getElasticsearchQuery(pk, request.user.groups.all())
    except Elkquery.DoesNotExist:
        return JsonResponse({ "error": { "message":"Query not found or not allowed"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        data["group"]=getUserGroup(request.user.groups.all())["id"]
        
        if ("sql" in data ):
            query.sql_ddl=None
        
        if ("sql_ddl" in data ):
            query.sql=None

        serializer = ElkquerySerializer(query, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateElasticsearchquery.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateElasticsearchquery.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('elkquery.add_elkquery', raise_exception=True)  
# POST elasticsearch_query/
def addElasticsearchquery(request, format=None):
   
    log.info('Start:'+addElasticsearchquery.__name__)

    try:
        data = JSONParser().parse(request)

        query=Elkquery()
        data["group"]=getUserGroup(request.user.groups.all())["id"]
        serializer=ElkquerySerializer(query, data=data)
        if serializer.is_valid():            
            serializer.save()
            log.info('End:'+addElasticsearchquery.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addElasticsearchquery.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["DELETE"])
@permission_required('elkquery.delete_elkquery', raise_exception=True)  
# DELETE elasticsearch_query/1/
def deleteElasticsearchquery(request, pk, format=None):
    log.info('Start:'+deleteElasticsearchquery.__name__)
    try:
        query=getElasticsearchQuery(pk, request.user.groups.all())
    except Elkquery.DoesNotExist:
        return JsonResponse({ "error": { "message":"Query not found or not allowed"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        query.delete()
        log.info('End:'+deleteElasticsearchquery.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('elkquery.execute_elkquery', raise_exception=True)  
# POST elasticsearch_query/execute/
def executeElasticsearchquery(request, format=None):
   
    log.info('Start:'+executeElasticsearchquery.__name__)

    try:
        data = JSONParser().parse(request)

        if ("sql_ddl" in data and data["sql_ddl"]):
            if getUserGroup(request.user.groups.all())["name"]!="administrator":
                raise ApiException("Query not allowed to be executed by user")
            
            data_sqlddl= json.loads(data["sql_ddl"])
            output=CustomElasticSearchQuery.executeDDL(data_sqlddl)
            return JsonResponse(output, status=status.HTTP_200_OK, safe=False)
        elif ("sql" in data) and data["sql"]:
            output=CustomElasticSearchQuery.executeSQL(data["sql"])
            return JsonResponse(output, status=status.HTTP_200_OK, safe=False)
    

        raise ApiException('Invalid parameters')
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

