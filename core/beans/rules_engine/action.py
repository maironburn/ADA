from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from condition.models import Condition
from django.http import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from core.utils.utils import Utils
import datetime
import traceback
import json

log = logging.getLogger(__name__)

class ActionImplementation():
    
    action=None

    def __init__(self, action ):
        self.action=json.loads(action)
 
    def executeAction(self, event):
        if self.action:
            value=None
            if self.action['type']=="assign":
                value=self.getFieldValue(event,self.action['value'])

                target=value
                fields=self.action['target'].strip().split('/')

                for item in reversed(fields):
                    objTmp={}
                    objTmp[item]=target
                    target= objTmp

                event=self.updateEvent(event, target)

            elif self.action['type']=="workflow":
                #recuperamos los valores
                workflow_method=self.getFieldValue(event,self.action['method'])
                parameters=self.action['parameters']
                
                try:

                    #Obtenemos el método que queremos lanzar
                    class_method_info=workflow_method.split(".")
                    exec_method=class_method_info[-1]
                    exec_class=class_method_info[-2]
                    exec_package=".".join(class_method_info[0:-2])
                    

                    local_var_command={}
                    import_command="from "+exec_package+ " import "+exec_class+"\n" 

                    #Recuperamos los parametros que se requieren para ejecutar el metodo
                    method_command="outputWF="+exec_class+"."+exec_method+".__code__.co_argcount"
                    exec_command=import_command + method_command
                    exec(exec_command,{}, local_var_command)
                    longitudJsonParameters=len(parameters)

                    # verficiamos si en el json vienen el mismo número de parámetros que necesita el workflow a ejecutar.
                    if local_var_command['outputWF'] != longitudJsonParameters:
                        raise ApiException("it is not have informed all parameters necessary to execute the method: " + exec_class + "."+ exec_method)
                    else:
                        #no se puede invocar al metodo pasándole el json directamente, hay que recoger cada uno de los parametros
                        #el último campo es la fecha por la que se quiere buscar, pero al venir como parámetro, se pasa como string entre comillas
                        inputsParameter=', '.join(key+'='+str(value) for key, value in parameters.items())
                        method_command="outputWF="+exec_class+"."+exec_method+"("+inputsParameter+")"
                        exec_command=import_command + method_command

                except Exception as e:
                    log.error('Exception:'+type(e).__name__ +" " +str(e))
                    log.error(traceback.format_exc())
                    return ApiException(str(e))

                exec(exec_command,{}, local_var_command)

                #se actualiza el evento con la información del resultado de cada una de las acciones
                actionName="action " + self.action['target']
                if 'action' in event:
                    event['action'].update({actionName:local_var_command['outputWF']})
                else:
                    event['action']={actionName:local_var_command['outputWF']}
    
        return event

    def getFieldValue(self, event, field):
        if field.__class__.__name__ == 'dict':  
            if "event_field" in field:
                return self.getEventFieldValue(event, field)
            elif "function"  in field:
                return self.getFunctionFieldValue(event, field)    
            else:
                return None    
        elif field.__class__.__name__ == 'str':
            return field.strip()
        else:
            return field  

    def getEventFieldValue(self, event, field):
        eventField=field['event_field'].strip()
        fields=eventField.split('/')
        obj=event
        for item in fields:
            if (obj.__class__.__name__ == 'dict'):
                if (item.strip() in obj):
                    obj=obj[item.strip()]
                else: 
                    return None
            else:
                if (hasattr(obj,item.strip())):
                    obj= getattr(obj, item.strip())
                else:
                    return None    
        return obj

    def getFunctionFieldValue(self, event, field):
        functionField= field['function']
        if "function_name" in functionField:

            output=None
            if functionField['function_name']=='lower':
                return self.executeFunctionLower(event,functionField['fields'])  
            elif functionField['function_name']=='concat':
                return self.executeFunctionConcat(event,functionField['fields'])  
            elif functionField['function_name']=='len':
                return self.executeFunctionLen(event,functionField['fields'])    
            elif functionField['function_name']=='replace':
                return self.executeFunctionReplace(event,functionField['fields'])
            elif functionField['function_name']=='trim':
                return self.executeFunctionTrim(event,functionField['fields'])
            elif functionField['function_name']=='upper':
                return self.executeFunctionUpper(event,functionField['fields'])
            elif functionField['function_name']=='substring':
                return self.executeFunctionSubstring(event,functionField['fields']) 
            else:
                raise ApiException("invalid function: " + functionField["function_name"])   
    
            return output
        else:
            return None

    def executeFunctionLower(self, event, fields):
        if (len(fields) == 1):
            return str(self.getFieldValue(event, fields[0])).lower()
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: lower")

    def executeFunctionConcat(self, event, fields):
        if (len(fields) == 2):
            output=str(self.getFieldValue(event, fields[0])) + str(self.getFieldValue(event, fields[1]))
            return output
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: concat")

    def executeFunctionLen(self, event, fields):
        if (len(fields) == 1):
            return len(str(self.getFieldValue(event, fields[0])))
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: len")
    
    def executeFunctionReplace(self, event, fields):
        if (len(fields) == 3):
            return str(self.getFieldValue(event, fields[0])).replace(str(self.getFieldValue(event, fields[1])),str(self.getFieldValue(event, fields[2])))
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: replace")

    def executeFunctionTrim(self, event, fields):
        if (len(fields) == 1):
            return str(self.getFieldValue(event, fields[0])).strip()
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: trim")

    def executeFunctionUpper(self, event, fields):
        if (len(fields) == 1):
            return str(self.getFieldValue(event, fields[0])).upper()
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: upper")

    def executeFunctionSubstring(self, event, fields):
        if (len(fields) == 3):
            return str(self.getFieldValue(event, fields[0]))[int(str(self.getFieldValue(event, fields[1]))):int(str(self.getFieldValue(event, fields[2])))]
        else:
            raise ApiException("invalid number of params ("+ str(len(fields)) +") for function: substring")
 
    def updateEvent(self, event, data):
        if Utils.getType(data)=='builtins':
            if Utils.getType(event)=='builtins':
                event=data
            else:
                #Es una asignacion incorrecta ya que intentamos meter un builtin en un objeto, no tocamos el evento
                pass 
            return event
        else:    
            if Utils.getType(event)=='builtins':
                event=data
                return event
            elif Utils.getType(event)=='dict':
                for key, value in data.items():
                    if key in event:
                        event[key]=self.updateEvent(event[key], value)
                    else:
                        event[key]=None
                        event[key]=self.updateEvent(event[key], value)
                    
                    return event
            elif Utils.getType(event)=='custom':
                for key, value in data.items():
                    if hasattr(event, key):
                        attr=getattr(event,key)
                        attr_value=self.updateEvent(attr, value)
                        setattr(event, key, attr_value)
                    else:   
                        #Es una asignacion incorrecta ya que intentamos meter un valor en un atributo inexistente en el objeto, no tocamos el evento
                        pass
                    return event
            else:
                return event


    def getFieldParameters(self, event, field):
        if field.__class__.__name__ == 'dict':  
            eventField=field['event_field'].strip()
            fields=eventField.split('/')
            obj=event
            for item in fields:
                if (item.strip() in obj):
                    obj=obj[item.strip()]
                else:
                    return None
            return obj
        elif field.__class__.__name__ == 'str':
            return field.strip()
        else:
            return field   

    

    

