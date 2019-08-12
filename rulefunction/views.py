from django.shortcuts import render
from rest_framework import status
from ApiADA.loggers import logging
from rest_framework.decorators import api_view
from .models import Rulefunction
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from .serializers import RulefunctionSerializer
import traceback


log = logging.getLogger(__name__)

def getRulefunction(pk):
    return Rulefunction.objects.get(pk=pk)

@api_view(["GET"])
@permission_required('rulefunction.view_rulefunction', raise_exception=True)  
# GET rulefunction/
def listRulefunction(request, format=None):
    try:
        log.info('Start:'+listRulefunction.__name__)

        rulefunction=Rulefunction.objects.all()
        serializer = RulefunctionSerializer(rulefunction, many=True)

        log.info('End:'+listRulefunction.__name__)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)

