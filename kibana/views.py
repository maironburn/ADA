from rest_framework import status
from .serializers import KibanaSerializer
from ApiADA.loggers import logging
from .models import Kibana
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from base64 import b64encode
from functools import reduce
import base64
import traceback
import binascii
import os
from django.conf import settings


log = logging.getLogger(__name__)


@api_view(["GET"])
@permission_required('kibana.view_kibana', raise_exception=True)  
# GET kibana/
def getUrl(request, format=None):
    try:
        log.info('Start:'+getUrl.__name__)

        profiles=request.user.groups.all()
        
        #Indicamos que en el filtro no haga distinction uppercase
        filter_list = map(lambda n: Q(perfil__iexact=n.name), profiles)
        filter_list = reduce(lambda a, b: a | b, filter_list)
        kibanas = Kibana.objects.filter(filter_list).order_by('priority')

        #serializer = KibanaSerializer(kibanas, many=True)

        kibanaUser=kibanas[0]
        connection_string='Base '+ kibanaUser.user+":"+kibanaUser.password

        auth_base64=base64.b64encode(connection_string.encode())
        auth_base64_str="".join( chr(x) for x in bytearray(auth_base64) )

        url=settings.KIBANA_URL

        log.info('End:'+getUrl.__name__)

        return JsonResponse({'url':url, 'sid':auth_base64_str}, status=status.HTTP_200_OK, safe=False)

        #return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)  

    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)
