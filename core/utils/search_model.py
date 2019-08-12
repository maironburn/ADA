from core.exceptions.customexceptions import SearchException
class SearchableModel:
     def search(model, filters):
        try:
            fields_searchable = model._meta.fields_searchable
            if fields_searchable == '__all__':
                fields_searchable=list(map(lambda itm: itm.name, model._meta.fields))

            fieldstoSearch={}
            objSearch=filters
            
            for key, value in filters.items():
                if key in fields_searchable:
                    fieldstoSearch[key]=value
            
            if len(fieldstoSearch)==0:
                raise SearchException("Unable to execute the search. There are not any allowed filters in search condition. ")
            else:
                return model.objects.filter(**fieldstoSearch)
        except SearchException as e:
            raise SearchException(str(e))
        except Exception:
            raise SearchException("Search not allowed in model.")