from django.shortcuts import render

from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Rule
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import RuleSerializer, RuleSerializerDeep
from rest_framework.parsers import JSONParser
from core.utils.search_model import SearchableModel
from core.exceptions.customexceptions import ApiException
from action.models import Action
import traceback

log = logging.getLogger(__name__)

def getRule(pk):
    return Rule.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    log.info('Start:'+getDataToUpdate.__name__)

    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    
    log.info('End:'+getDataToUpdate.__name__)
    return merged_data

@api_view(["GET","POST"])
@permission_required('rule.view_rule','rule.add_rule', raise_exception=True)  
def actionRule(request, format=None):
    if request.method=='GET':
        return listRules(request._request)
    elif request.method=='POST':
        return addRule(request._request)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["PUT", "DELETE"])
@permission_required('rule.change_rule','rule.delete_rule', raise_exception=True)  
def modifyRule(request, pk, format=None):
    if request.method=='PUT':
        return updateRule(request._request, pk=pk)
    elif request.method=='DELETE':
        return deleteRule(request._request, pk=pk)
    else:
        return JsonResponse({ "error": { "message":  'Method not allowed'} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["GET"])
@permission_required('rule.view_rule', raise_exception=True)  
# GET rule/
def listRules(request, format=None):
    try:
        log.info('Start:'+listRules.__name__)

        rules=Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)

        log.info('End:'+listRules.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('rule.view_rule', raise_exception=True)  
# POST rule/search/
def searchRules(request, format=None):
    
    log.info('Start:'+searchRules.__name__)

    try:
        data = JSONParser().parse(request)
        resultado=SearchableModel.search(Rule,data)
        serializer=RuleSerializer(resultado, many=True)

        log.info('End:'+searchRules.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)       

@api_view(["POST"])
@permission_required('rule.view_rule', raise_exception=True)  
# POST rule/searchdetails/
def searchRulesDetails(request, format=None):
    
    log.info('Start:'+searchRulesDetails.__name__)

    try:
        data = JSONParser().parse(request)
        resultado=SearchableModel.search(Rule,data)
        serializer=RuleSerializerDeep(resultado, many=True)

        log.info('End:'+searchRulesDetails.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)           

@api_view(["PUT"])
@permission_required('rule.change_rule', raise_exception=True)  
# Put rule/1/
def updateRule(request, pk, format=None):

    log.info('Start:'+updateRule.__name__)
    try:
        rule=getRule(pk)
    except Rule.DoesNotExist:
        return JsonResponse({ "error": { "message":"Rule not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        merged_data=getDataToUpdate(RuleSerializer(rule).data, data)

        serializer = RuleSerializer(rule, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateRule.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+updateRule.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('rule.add_rule', raise_exception=True)  
# POST rule/
def addRule(request, format=None):
   
    log.info('Start:'+addRule.__name__)

    try:
        data = JSONParser().parse(request)

        rule=Rule()
        serializer=RuleSerializer(rule, data=data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+addRule.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            msg=''
            if len(serializer.errors) > 0:
                    for error in serializer.errors:
                        msg=error+':'+",".join(serializer.errors[error])
            else:
                msg='Unknown Error'
            raise ApiException(msg)

        log.info('End:'+addRule.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["DELETE"])
@permission_required('rule.delete_rule', raise_exception=True)  
# DELETE rule/1/
def deleteRule(request, pk, format=None):
    log.info('Start:'+deleteRule.__name__)
    try:
        rule=getRule(pk)
    except Rule.DoesNotExist:
        return JsonResponse({ "error": { "message":"Rule not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        rule.delete()
        log.info('End:'+deleteRule.__name__)
        return JsonResponse(None, status=status.HTTP_204_NO_CONTENT, safe=False)

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["POST"])
@permission_required('rule.change_rule', raise_exception=True)  
# POST rule/1/reorderactions/
def reorderRuleActions(request,pk,format=None):        
    try:
        log.info('Start:'+reorderRuleActions.__name__)

        try:
            rule=getRule(pk)
            actions=SearchableModel.search(Action,{'rule':rule.id})
        except Rule.DoesNotExist:
            return JsonResponse({ "error": { "message":"Rule not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

        data = JSONParser().parse(request)
        for action in actions:
            dataAction=list(filter(lambda x: x["id"] == action.id, data))
            if len(dataAction)>0:
                action.order=dataAction[0]["order"]
                action.save()

        rule=getRule(pk)
        serializer = RuleSerializer(rule)

        log.info('End:'+reorderRuleActions.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)  