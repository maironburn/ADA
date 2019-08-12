from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from ApiADA.constantes import Constantes

class AnalysisInfoSerializer(serializers.Serializer):
       last_analysis_date = serializers.DateTimeField(write_only=True, required=True)
       last_case_timestamp = serializers.DateTimeField(write_only=True, required=True)
       queue = serializers.CharField(write_only=True)
       
       def to_internal_value(self, data):
            output={}
            if ("last_analysis_date" in data) and (data["last_analysis_date"] != None):
                    output["last_analysis_date"]=data["last_analysis_date"].strftime(Constantes.DATETIME_FORMAT)

            if ("last_case_timestamp" in data) and (data["last_case_timestamp"] != None):
                    output["last_case_timestamp"]=data["last_case_timestamp"].strftime(Constantes.DATETIME_FORMAT)
            if ("queue" in data and (data["queue"]!= None)):
                    output["queue"] = data["queue"]


            return output
   
