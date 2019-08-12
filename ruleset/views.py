from rest_framework import status
from .serializers import RulesetSerializer
from core.utils.search_model import SearchableModel
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Ruleset
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from rest_framework.parsers import JSONParser
import traceback
from rule.models import Rule


log = logging.getLogger(__name__)

def getRuleSet(pk):
    return Ruleset.objects.get(pk=pk)

def getDataToUpdate(initial_data, data):
    merged_data=initial_data
    if "id" in data:
        del data["id"]
    
    merged_data.update(data)
    return merged_data

@api_view(["GET"])
@permission_required('ruleset.view_ruleset', raise_exception=True)  
# GET ruleset/
def listRuleSet(request, format=None):
    try:
        log.info('Start:'+listRuleSet.__name__)

        rulesets = Ruleset.objects.all()
        serializer = RulesetSerializer(rulesets, many=True)

        log.info('End:'+listRuleSet.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)


@api_view(["GET"])
@permission_required('ruleset.view_ruleset', raise_exception=True)  
# GET ruleset/1/detail/
def detailRuleSet(request, pk, format=None):
    try:
        log.info('Start:'+detailRuleSet.__name__)
        ruleset=getRuleSet(pk)
        serializer = RulesetSerializer(ruleset)

        log.info('End:'+detailRuleSet.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)        



@api_view(["PUT"])
@permission_required('ruleset.change_ruleset', raise_exception=True)  
# PUT ruleset/1/
def updateRuleSet(request, pk, format=None):
    
    log.info('Start:'+updateRuleSet.__name__)
    try:
        ruleset=getRuleSet(pk)
    except ruleset.DoesNotExist:
        return JsonResponse({ "error": { "message":"RuleSet not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

    try:
        data = JSONParser().parse(request)

        data['modified_by']=request.user.username

        merged_data=getDataToUpdate(RulesetSerializer(ruleset).data, data)

        serializer = RulesetSerializer(ruleset, data=merged_data)
        if serializer.is_valid():
            serializer.save()
            log.info('End:'+updateRuleSet.__name__)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

        log.info('End:'+updateRuleSet.__name__)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

@api_view(["POST"])
@permission_required('ruleset.view_ruleset', raise_exception=True)  
# POST ruleset/search/
def searchRuleset(request, format=None):
    
    log.info('Start:'+searchRuleset.__name__)

    try:
        data = JSONParser().parse(request)
        data["hidden"]=False
        resultado=SearchableModel.search(Ruleset,data)
        serializer=RulesetSerializer(resultado, many=True)

        log.info('End:'+searchRuleset.__name__)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)        

  

@api_view(["POST"])
@permission_required('ruleset.change_ruleset', raise_exception=True)  
# POST ruleset/1/reorder/
def reorderRuleset(request,pk,format=None):        
    try:
        log.info('Start:'+reorderRuleset.__name__)

        try:
            ruleset=getRuleSet(pk)
            rules=SearchableModel.search(Rule,{'ruleset':ruleset.id})
        except Ruleset.DoesNotExist:
            return JsonResponse({ "error": { "message":"RuleSet not found"} }, status=status.HTTP_400_BAD_REQUEST, safe=False)

        data = JSONParser().parse(request)
        for rule in rules:
            dataRules=list(filter(lambda x: x["id"] == rule.id, data))
            if len(dataRules)>0:
                rule.order=dataRules[0]["order"]
                rule.save()

        ruleset=getRuleSet(pk)
        serializer = RulesetSerializer(ruleset)

        log.info('End:'+reorderRuleset.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)  


 