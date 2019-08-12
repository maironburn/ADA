from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from ruleset.models import Ruleset
from core.beans.rules_engine.rule import RuleImplementation
from rule.models import Rule
import traceback
import json
from json_tricks import dumps
from appparameter.models import Appparameter

log = logging.getLogger(__name__)


class RulesetImplementation():

    objRuleset=None

    def __init__(self, objRuleset ):
        self.objRuleset=objRuleset


    def executeRuleset(self, event):
        log.info('Start: executeRuleset')
        
        output=False
        try:
            for rule in Rule.objects.filter(ruleset=self.objRuleset.id, status=True).order_by('order').all():
                ruleImplementation=RuleImplementation(rule)
                output=ruleImplementation.verifyRule(event)
                
                if (output):
                    ruleImplementation.executeAction(event)
                    break
        
        except Exception as e:
                log.error('Exception:'+type(e).__name__ +" " +str(e))
                log.error(traceback.format_exc())
                raise ApiException(str(e)) 

        log.info('End: executeRuleset')


class RulesetAux():

    reVerifyFieldPattern=None

    def setFieldPatterValidator():
        #obtenemos el valor de la variable de la expresión regular
        reVerifyPatternParam_param=Appparameter.objects.get(name='Field pattern validator')
        reVerifyPatternParam=reVerifyPatternParam_param.getParamaterDataValue()

        RulesetImplementationAux.reVerifyFieldPattern=reVerifyPatternParam

