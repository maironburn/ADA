from rest_framework import serializers
from ApiADA.constantes import Constantes

class ElasticSearchSerializer(serializers.Serializer):
       def to_internal_value(self, data):
            output={}
            for item in data:
                     obj=data[item]
                     output[item]=self.getValueObject(obj)
                            
            return output
   
       def getValueObject(self, data):
              if data.__class__.__name__ == 'TableCase':
                     from core.vodafone.smart.case.serializers import TableCaseSerializer
                     serializer=TableCaseSerializer(data)    
                     return serializer.data
              elif data.__class__.__name__ == 'TableQueue':
                     from core.vodafone.smart.queue.serializers import TableQueueSerializer
                     serializer=TableQueueSerializer(data)    
                     return serializer.data
              elif data.__class__.__name__ == 'Contract':
                     from core.vodafone.smart.contract.serializers import ContractSerializer
                     serializer=ContractSerializer(data)    
                     return serializer.data
              elif data.__class__.__name__ == 'Site':
                     from core.vodafone.smart.site.serializers import SiteSerializer
                     serializer=SiteSerializer(data)    
                     return serializer.data  
              elif data.__class__.__name__ == 'Validation':
                     from core.validation.serializers import ValidationSerializer
                     serializer=ValidationSerializer(data)    
                     return serializer.data                       
              elif data.__class__.__name__ == 'int':       
                     return data
              elif data.__class__.__name__ == 'float':       
                     return data    
              elif data.__class__.__name__ == 'str':       
                     return data      
              elif data.__class__.__name__ == 'bool':       
                     return data   
              elif ((data.__class__.__name__ == 'date') or (data.__class__.__name__ =='datetime')):       
                      return data.strftime(Constantes.DATETIME_FORMAT)
              elif ((data.__class__.__name__ == 'dict') or (data.__class__.__name__ == 'OrderedDict')):     
                     output_dict={}
                     for key, value in data.items():
                            output_dict[key]=self.getValueObject(value)
                     return output_dict
              elif data.__class__.__name__ == 'list':     
                     output_list=[]
                     for value in data:
                            output_list.append(self.getValueObject(value))
                     return output_list 
              elif data.__class__.__name__ == 'NoneType':
                     return None      
              else:
                     return data   

class ElasticSearchToDictSerializer(serializers.Serializer):
    
    def to_internal_value(self, data):
        output = { }
        for (key, value) in data.items():
            self.setValue(value, key, output)
        
        return output

    
    def setValue(self, data, key, objDict):
        elems = key.split('.')
        if elems[0] in objDict:
            if len(elems) > 1:
                self.setValue(data, '.'.join(elems[1:]), objDict[elems[0]])
            else:
                objDict[elems[0]] = data
        elif len(elems) > 1:
            objDict[elems[0]] = { }
            self.setValue(data, '.'.join(elems[1:]), objDict[elems[0]])
        else:
            objDict[elems[0]] = data
       

