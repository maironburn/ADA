from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from .serializers import LoginSerializer
from ApiADA.loggers import logging
from rest_framework.decorators import  permission_classes, api_view
from .models import User
from tokencontrol.models import Tokencontrol
from core.vodafone.vf_authentication.beans import VFAuthentication
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import Group
import traceback
import json
import jwt
import datetime

log = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes((AllowAny,))  
def login(request, format=None):
    try:
        log.info('Start:'+__name__+"."+login.__name__)
        userlogin = request.data.get('login', None)
        password = request.data.get('password', None)
        override = request.data.get('override', None)

        override = True if override and override.strip()=='1' else False 

        if (( not userlogin)  or (userlogin.strip() == '')):
            raise Exception ("Login is required")
        if (( not password)  or (password.strip() == '')):
            raise Exception ("Password is required")

        vfAuth= VFAuthentication()
        user_info = vfAuth.authenticatVFUser(username=userlogin, password=password)

        old_groups=[]
        try:
            objUser=User.objects.get(username=user_info['username'])

   
            #Verificamos si ya existe un token para el usuario
            try:
                objToken=Tokencontrol.objects.get(user_id=objUser.id)    
                if (override):
                    objToken.delete()
                else:
                    try:
                        payload = jwt.decode(objToken.token, settings.SECRET_KEY)
                        return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
                    except jwt.ExpiredSignatureError:
                        objToken.delete()    
                    except:
                        return JsonResponse({ "error": { "message":"Error verifying current user session."} }, status=status.HTTP_400_BAD_REQUEST, safe=False)
            except Tokencontrol.DoesNotExist as e:
                pass

            #Si superamos la validacion del token, continuamos con el resto de acciones del logado
            objUser.firstname=user_info['firstname']
            objUser.surname=user_info['surname']
            objUser.set_password(settings.DEFAULT_PWD)
            objUser.last_login=datetime.datetime.now()
            objUser.save()

            old_groups=objUser.user_groups

        except User.DoesNotExist as e:
            objUser=User.objects.create_user( username=user_info['username'], email=user_info['email'], password=settings.DEFAULT_PWD, firstname=user_info['firstname'], surname=user_info['surname'])




        new_groups=list(map(lambda x: vfAuth.mapGroup(x),  user_info['groups']))

        for group in old_groups:
            if group in new_groups:
                pass
            else:
                objGroup=Group.objects.get(name=group)
                objUser.groups.remove(objGroup)

        for group in new_groups:
             if group in old_groups:
                 pass
             else:    
                objGroup=Group.objects.get(name=group)
                objUser.groups.add(objGroup)       


        user= {'email':objUser.email, 'password':settings.DEFAULT_PWD}

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = LoginSerializer(data=user)
        serializer.is_valid(raise_exception=True)


        #Guardamos el token en la BBDD
        objToken=Tokencontrol()
        objToken.token=serializer.validated_data['token']
        objToken.user_id=objUser.id
        objToken.save()
       
        


        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK)        
    except Exception as e:
        log.error('Exception:'+type(e).__name__ +" " +str(e))
        log.error(traceback.format_exc())
        return JsonResponse({ "error": { "message":  str(e) } }, status=status.HTTP_400_BAD_REQUEST, safe=False)
        
  
@api_view(["POST"])
def logout(request, format=None):
    try:
        user_id=request.user.id

        #Verificamos si ya existe un token para el usuario
        try:
            objToken=Tokencontrol.objects.get(user_id=user_id)    
            objToken.delete()
        except Tokencontrol.DoesNotExist as e:
            pass
    except:
        pass

    return JsonResponse({}, status=status.HTTP_200_OK, safe=False)
