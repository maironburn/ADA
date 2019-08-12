from django.core.exceptions import ValidationError
import json


class ApiADAValidator():

    def validateJSONField(value):

        try:
            field=json.loads(value)
            return True
        except Exception as e:
            raise ValidationError("Invalid JSON value: "+str(value)+ " Error:"+str(e))   
        