from django.core.exceptions import ValidationError
import json
from json_tricks import dumps
from core.exceptions.customexceptions import ApiException

class ActionValidator():

    def validateFields(value):

        fields=[]
        if (not value):
            raise ValidationError("Invalid value. "+str(value))

        if (value) and (value.__class__.__name__=="str"):
            return True

        fields=value if value.__class__.__name__ == "list" else [value]

        for field in fields:
            if field.__class__.__name__ == "dict":
                if "function" in field:
                    if not "function_name" in field["function"]:
                        raise ValidationError("A function requires a function_name property. "+dumps(field)) 

                    if (not "fields" in field["function"]) or (len(field["function"]["fields"])==0):
                        raise ValidationError("A function requires a fields property. "+dumps(field)) 
                
                    for param in field["function"]["fields"]:
                        ActionValidator.validateFields(param)

                elif "event_field" in field:
                    if (field["event_field"].strip()==""):
                        raise ValidationError("An event_field requires a not blank value. "+dumps(field))
                elif "workflow" in field:
                    if not "id" in field["workflow"]:
                        raise ValidationError("A workflow requires a not blank id. "+dumps(field))
                    if not "name" in field["workflow"]:
                        raise ValidationError("A workflow requires a not blank name. "+dumps(field))
                    if not "parameters" in field["workflow"]:
                        raise ValidationError("A workflow requires a not blank parameters. "+dumps(field))
                else:
                    raise ValidationError("Invalid value/field. "+dumps(field))       
            else:
                return True    


    def validateAction(value):

        action=json.loads(value)

        if (not "type" in  action):
             raise ValidationError("An action required a type property. "+dumps(action))

        if (action["type"]!="assign"):     
            raise ValidationError("The action type should be one 'assign'. "+dumps(action))

        if (not "value" in action):
            raise ValidationError("An 'assign' action requires a value property. "+dumps(action))
            
        if (action["value"]):
            if ("workflow" in action["value"]):
                if ("target" in action):
                    raise ValidationError("A 'workflow' action mustn't have target. "++dumps(action))
            else:
                if (not "target" in action or len(action["target"])==0):
                    raise ValidationError("An 'assign' action requires a target property. "+dumps(action))

        return ActionValidator.validateFields(action["value"])
