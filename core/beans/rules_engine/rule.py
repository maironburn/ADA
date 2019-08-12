from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from rule.models import Rule
from core.beans.rules_engine.condition import ConditionImplementation
from core.beans.rules_engine.action import ActionImplementation
from condition.models import Condition
from action.models import Action
import traceback
import json
from json_tricks import dumps

from django.http import JsonResponse
from rest_framework import status

log = logging.getLogger(__name__)


class RuleImplementation():

    objRule=None

    def __init__(self, objRule ):
        self.objRule=objRule


    def verifyRule(self, event):
        log.info('Start: verifyRule Description:'+self.objRule.description)

        #condition=Condition.objects.filter(rule=self.objRule.id)[0]
        tmp=True
        if (self.objRule.condition_id):
            condition=Condition.objects.filter(id=self.objRule.condition_id)[0]
            if (condition):
                conditionImpletantion=ConditionImplementation(condition)
                tmp=conditionImpletantion.verifyCondition(event)
            else:
                raise ApiException('Condition with id %s not found' % self.objRule.condition_id)
            

        log.info('End: verifyRule Description:'+self.objRule.description+' Output:'+str(tmp))

        return tmp

    def executeAction(self, event):
        log.info('Start: executeAction Description:'+self.objRule.description)
        #Recogemos las acciones que tiene nuestra regla 
        #actions=Action.objects.filter(rule=self.objRule.id).order_by('order').all()
        if (self.objRule.id):
            actions=Action.objects.filter(rule=self.objRule.id).order_by('order').all()

            try:
                tmp=event
                for action in actions:
                    actionImplementation=ActionImplementation(action.logicalaction)
                    tmp=actionImplementation.executeAction(event)
                
                log.info('End: executeAction Description:'+self.objRule.description)
                return tmp

            except Exception as e:
                    log.error('Exception:'+type(e).__name__ +" " +str(e))
                    log.error(traceback.format_exc())
                    raise ApiException(str(e)) 
        else:
            log.info('End: executeAction Description:'+self.objRule.description)
            return event




        

