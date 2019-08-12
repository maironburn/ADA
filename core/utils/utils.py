class Utils:
     
    #
    #   Method to get the type of an object
    #   inputs:
    #       obj: object to verify
    #   output:
    #       string: 
    #           'builtins' - if the object is a python predefined type different from dict and list
    #           'dict' - if the object is a dict
    #           'list' - if the object is a list
    #           'custom' - if the object is a custom object     
    def getType(obj):
        tmp=type(obj).__module__

        if (tmp == 'builtins'):
            if obj.__class__.__name__ == 'list':
               return 'list'
            elif obj.__class__.__name__ == 'dict':     
                return 'dict'
            elif obj.__class__.__name__ == 'OrderedDict':     
                return 'OrderedDict'
            else:
                return 'builtins'    

        else:
            return 'custom'    