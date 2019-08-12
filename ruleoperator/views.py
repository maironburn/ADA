from django.shortcuts import render
from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Ruleoperator
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import RuleoperatorSerializer
import traceback
from rest_framework.parsers import JSONParser
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

def getRuleoperator(pk):
    return Ruleoperator.objects.get(pk=pk)

@api_view(["GET"])
@permission_required('ruleoperator.view_ruleoperator', raise_exception=True)  
# GET ruleoperator/
def listRuleoperator(request, format=None):
    try:
        log.info('Start:'+listRuleoperator.__name__)

        ruleoperator=Ruleoperator.objects.all()
        serializer = RuleoperatorSerializer(ruleoperator, many=True)

        log.info('End:'+listRuleoperator.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)