from ApiADA.loggers import logging
from django.core.exceptions import ValidationError
import json
from json_tricks import dumps
from ruleoperator.models import Ruleoperator
from core.exceptions.customexceptions import ApiException


log = logging.getLogger(__name__)

class ConditionValidator():

    def validateCondition(value):

        log.info('Start:validateCondition')

        condition=json.loads(value)

        if (not "type" in  condition):
             raise ValidationError("A condition required a type property. "+dumps(condition))

        if (condition["type"]!="and" and condition["type"]!="or" and condition["type"]!="not" and condition["type"]!="simple"):     
            raise ValidationError("The condition type should be one of 'and','or','not', 'simple'. "+dumps(condition))

        if (condition["type"]=="and"):
            if (not "conditions" in condition or len(condition["conditions"])<2):
                raise ValidationError("An AND condition should have at least two children conditions. "+dumps(condition))
            
            for cond in condition["conditions"]: 
                ConditionValidator.validateCondition(dumps(cond)) 

        if (condition["type"]=="or"):
            if (not "conditions" in condition or len(condition["conditions"])<2):
                raise ValidationError("A OR condition should have at least two children conditions. "+dumps(condition))
            
            for cond in condition["conditions"]: 
                ConditionValidator.validateCondition(dumps(cond)) 
    
        if (condition["type"]=="not"):
            if ((not "conditions" in condition) or (len(condition["conditions"])!=1)):
                raise ValidationError("A NOT condition should have only one child condition. "+dumps(condition))
            
            for cond in condition["conditions"]: 
                ConditionValidator.validateCondition(dumps(cond)) 

        if (condition["type"]=="simple"):
            if ("conditions" in condition and len(condition["conditions"])>0):
                raise ValidationError("A SIMPLE condition should not have any child condition. "+dumps(condition))
            if (not "condition_simple" in condition):
                raise ValidationError("A SIMPLE condition should have one condition simple. "+dumps(condition))
            if (not "operator" in condition["condition_simple"]):
                raise ValidationError("A SIMPLE condition should have one operator. "+dumps(condition["condition_simple"]))

            try:
                operator=Ruleoperator.objects.get(operator=condition["condition_simple"]["operator"])

                #Si encontramos el operador
                numFields=operator.numfields
                if (numFields == 1):
                    if (not "field1" in condition["condition_simple"]):
                        raise ValidationError("For operator "+ condition["condition_simple"]["operator"] + " is required field1. "+dumps(condition["condition_simple"]))
                    if ((condition["condition_simple"]["field1"].__class__.__name__ == "dict") and ( not "event_field" in condition["condition_simple"]["field1"])):
                        raise ValidationError("The value for field1 is invalid. " +dumps(condition["condition_simple"]))

                elif (numFields == 2):
                    if ((not "field1" in condition["condition_simple"]) or (not "field2" in condition["condition_simple"])):
                        raise ValidationError("For operator "+ condition["condition_simple"]["operator"] + " is required field1 and field2. "+dumps(condition["condition_simple"]))
                    if ((condition["condition_simple"]["field1"].__class__.__name__ == "dict") and ( not "event_field" in condition["condition_simple"]["field1"])):
                        raise ValidationError("The value for field1 is invalid. "+dumps(condition["condition_simple"]))
                    if ((condition["condition_simple"]["field2"].__class__.__name__ == "dict") and ( not "event_field" in condition["condition_simple"]["field2"])):
                        raise ValidationError("The value for field2 is invalid. " +dumps(condition["condition_simple"]) )

            except Ruleoperator.DoesNotExist:
                raise ValidationError("The operator is not valid. "+dumps(condition["condition_simple"]))

            
        log.info('End:validateCondition')

        return True
