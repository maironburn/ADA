"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
import yaml
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import ContentType


class Command(BaseCommand):
    help = 'Creates default permission groups for users'

    def handle(self, *args, **options):
        #we create a variable with the path our config application file
        #with "yaml" library, we open application config file on read mode
        permissions_config=yaml.safe_load(open(os.path.join(settings.CONFIG_DIR,"permissions.yml"), "r"))
        #LOG_LEVEL = application_config[API_ENVIRONMENT]["LOG_LEVEL"]
        #DEFAULT_PWD= application_config[API_ENVIRONMENT]["DEFAULT_PWD"]
        print (permissions_config)

        all_groups=permissions_config['info']['groups']
        all_models=permissions_config['info']['models']
        all_permissions=permissions_config['info']['permissions']

        for group in all_groups:
            new_group, created = Group.objects.get_or_create(name=group)
            new_group_default_permissions=permissions_config[group]['default']
            new_group.permissions.clear()
            for model in all_models:
                try:
                    permissions=permissions_config[group][model]['permissions']
                    print('Añado del fichero el permiso:'+",".join(permissions)+' del group:'+group+' del modelo:'+model)  

                except KeyError:
                    permissions=new_group_default_permissions
                    print('Añado del default el permiso:'+",".join(permissions)+' del group:'+group+' del modelo:'+model)  
                for permission in permissions:
                    name =  'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))
                    
                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        model_add_perm=Permission()
                        model_add_perm.content_type=ContentType.objects.get(model=model)
                        model_add_perm.codename=permission+"_"+model
                        model_add_perm.name=name
                        model_add_perm.save()
                        continue
                    except Exception as e:
                        print("Error creating the permission with name %s Error: %s" %(name, str(e)) )

                    new_group.permissions.add(model_add_perm)

      
