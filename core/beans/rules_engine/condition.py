from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from condition.models import Condition
import traceback
import json
import re
from json_tricks import dumps
from ApiADA.constantes import Constantes
from core.beans.rules_engine.rulesetAux import RulesetAux

log = logging.getLogger(__name__)


class ConditionImplementation():
    
    logicalCondition=None

    def __init__(self, objCondition ):
        if objCondition. __class__.__name__ == 'Condition':
            self.logicalCondition=json.loads(objCondition.logicalcondition)
        else:
            self.logicalCondition=objCondition

    def verifyCondition(self, event):
        
        output=False
        if self.logicalCondition['type']=='simple':
            output=self.verifyConditionSimple(event,self.logicalCondition['condition_simple'])    
        elif self.logicalCondition['type']=='and':   
            output=self.verifyConditionAnd(event,self.logicalCondition['conditions'])    
        elif self.logicalCondition['type']=='or':   
            output=self.verifyConditionOr(event,self.logicalCondition['conditions'])    
        elif self.logicalCondition['type']=='not':   
            output=self.verifyConditionNot(event,self.logicalCondition['conditions'])             


        return output

    def verifyConditionSimple(self, event, condition):
        output=False
        if (condition['operator']=='='):
            output=self.verifyConditionSimpleEqual(event,condition['field1'],condition['field2'])

        elif (condition['operator']=='#'):
            output=self.verifyConditionSimpleEqualIgnoreCase(event,condition['field1'],condition['field2'])

        elif (condition['operator']=='<>'):
            output=self.verifyConditionSimpleNotEqual(event,condition['field1'],condition['field2'])
        
        elif (condition['operator']=='>'):
            output=self.verifyConditionSimpleGreat(event,condition['field1'],condition['field2'])

        elif (condition['operator']=='>='):
            output=self.verifyConditionSimpleGreatOrEqual(event,condition['field1'],condition['field2'])

        elif (condition['operator']=='<'):
            output=self.verifyConditionSimpleLess(event,condition['field1'],condition['field2'])
        
        elif (condition['operator']=='<='):
            output=self.verifyConditionSimpleLessOrEqual(event,condition['field1'],condition['field2'])
        
        elif (condition['operator']=='like'):
            output=self.verifyConditionSimpleLike(event,condition['field1'],condition['field2'])
        elif (condition['operator']=='exists'):
            output=self.verifyConditionSimpleExists(event,condition['field1'])
        elif (condition['operator']=='in'):
            output=self.verifyConditionSimpleIn(event,condition['field1'],condition['field2'])

        return output

    def verifyConditionAnd(self, event, conditions):
        output=True
        for cond in conditions:
            objCond=ConditionImplementation(cond)
            output=objCond.verifyCondition(event)
            if (not output):
                break
        return output

    def verifyConditionOr(self, event, conditions):
        output=False
        for cond in conditions:
            objCond=ConditionImplementation(cond)
            output=objCond.verifyCondition(event)
            if (output):
                break
        return output


    def verifyConditionNot(self, event, conditions):
        output=False
        for cond in conditions:
            objCond=ConditionImplementation(cond)
            output=objCond.verifyCondition(event)
            return not output
        return output

        #objCond=ConditionImplementation(conditions)
        #return objCond.verifyCondition(event)

    def verifyConditionSimpleEqual(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            return str(field1Value)==str(field2Value)    
    
    def verifyConditionSimpleEqualIgnoreCase(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:  
            return str(field1Value).upper()==str(field2Value).upper()  


    def verifyConditionSimpleNotEqual(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            return str(field1Value)!=str(field2Value)    
    
    def verifyConditionSimpleGreat(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            try:
                return float(str(field1Value)) > float(str(field2Value))  
            except Exception:  
                return str(field1Value) > str(field2Value)

    def verifyConditionSimpleGreatOrEqual(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            try:
                return float(str(field1Value)) >= float(str(field2Value))  
            except Exception:  
                return str(field1Value) >= str(field2Value)

    def verifyConditionSimpleLess(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            try:

                return float(str(field1Value)) < float(str(field2Value))  
            except Exception:
                return str(field1Value) < str(field2Value)
    
    def verifyConditionSimpleLessOrEqual(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        
        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            try:
                return float(str(field1Value)) <= float(str(field2Value))  
            except Exception:  
                  return str(field1Value) <= str(field2Value)

    def verifyConditionSimpleLike(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)

        if ((field1Value is None) or (field2Value is None)):
            return False
        else:
            #field1 is the text
            #field2 is the pattern
            #verifyFieldPattern=Constantes.FIELD_PATTERN_VALIDATOR

            #
            verifyFieldPattern=RulesetAux.reVerifyFieldPattern
            if (verifyFieldPattern.match(field2Value)):
                field2Valuesearch=".*"+field2Value+".*"
                reField=re.compile(field2Valuesearch, re.IGNORECASE)
                isMatching=reField.match(field1Value)
                if (isMatching):
                    return True
                else:
                    return False
            else:
                return False



    def getFieldValue(self, event, field):
        if field.__class__.__name__ == 'dict':  
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
        elif field.__class__.__name__ == 'str': 
            return field.strip()
        else:
            return field               
 

    def verifyConditionSimpleExists(self, event, field1):

        field1Value=self.getFieldValue(event, field1)
        
        if (field1Value is None):
            return False
        else:
            return True
 
 

    def verifyConditionSimpleIn(self, event, field1, field2):
        output=False
        field1Value=self.getFieldValue(event, field1)
        field2Value=self.getFieldValue(event, field2)
        
        if ((field1Value is None) or (field2Value is None)):
            return False
        elif (field2Value.__class__.__name__ != 'list'):
            return False
        else:
            try:
                return field1Value in field2Value
            except Exception:  
                return False


