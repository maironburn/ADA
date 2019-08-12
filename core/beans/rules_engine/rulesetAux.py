from appparameter.models import Appparameter
import re




class RulesetAux():

    reVerifyFieldPattern=None

    def setFieldPatternValidator():
        #obtenemos el valor de la variable de la expresión regular
        reVerifyPatternParam_param=Appparameter.objects.get(name='Field pattern validator')
        reVerifyPatternParam=reVerifyPatternParam_param.getParamaterDataValue()

        RulesetAux.reVerifyFieldPattern=re.compile(reVerifyPatternParam,re.IGNORECASE)

