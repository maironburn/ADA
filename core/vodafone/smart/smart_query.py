from django.db import connections
import traceback
from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException
from django.db.utils import OperationalError
from collections import namedtuple

log = logging.getLogger(__name__)

def my_custom_sql(database, sql):
    try:

        try:
            with connections[database].cursor() as cursor:
                cursor.execute(sql)
                results = dictfetchall(cursor)

            return results
        except OperationalError as e:
            connections[database].close()
            connections[database].ensure_connection()
            with connections[database].cursor() as cursor:
                cursor.execute(sql)
                results = dictfetchall(cursor)

            return results

    except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0].lower() for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


#   Metodo para ejecutar un PL/SQL de tipo procedure en la BBDD
#   inputs:
#       database: identificador de la BBBDD donde se ejecuta el procedure
#       procedure: nombre del procedimiento a ejecutar (scehma.procedure) 
#       params: array con los parametros del procedimiento
#               Array de objetos JSON con formatp
#               {
#                       "name": Nombre del parametro
#                       "inout": Direccion del parametro IN para parametros de entrada OUT para parametros de salida
#                       "type": Tipo de dato (String o Number) 
#                       "value": Valor del parametro (solo para los parametros de entrada)
#               }    
#   output:
#       return dict con los datos de entrada+salida del procedimiento
# 
def execProcedure(database, procedure, params):
    
    try:    
        results={}
        code="import cx_Oracle\n"
        proc_params=[]
        for param in params:
            if param["inout"]=='IN':
                if param["type"] == 'String':
                    code=code+ param["name"] + "='" + str(param["value"]) + "'\n" 
                else:
                    code=code+ param["name"] + "=" + str(param["value"]) + "\n"     
                
                proc_params.append(param["name"])
            else:  
                if param["type"] == 'String':
                    code=code+ param["name"] + "=cursor.var(cx_Oracle.STRING)\n" 
                elif param["type"] == 'Number':        
                    code=code+ param["name"] + "=cursor.var(cx_Oracle.NUMBER)\n" 
                
                proc_params.append(param["name"])
 
        code=code+"cursor.callproc('"+ procedure+ "',["+ ",".join(proc_params)+"])\n"
        code=code+"output={}\n"

        for param in params:
            if param["inout"]=='IN':
                if param["type"] == 'String':
                    code=code+ "output['" + param["name"] + "']='"+str(param["value"])+"'\n"
                else:
                    code=code+ "output['" + param["name"] + "']="+str(param["value"])+"\n" 
                
            else:   
                code=code+ "output['" + param["name"] + "']="+param["name"]+".getvalue()\n"

        
        try:
            djangoCursor=connections[database].cursor()
            cursor=djangoCursor.connection.cursor()
            
            local_var_command={}
            local_var_command['cursor']=cursor
            exec(code,{}, local_var_command)
            results=local_var_command['output']
        except OperationalError as e:
            connections[database].close()
            connections[database].ensure_connection()
            djangoCursor=connections[database].cursor()
            cursor=djangoCursor.connection.cursor()
            
            local_var_command={}
            local_var_command['cursor']=cursor
            exec(code,{}, local_var_command)
            results=local_var_command['output']

 
        return results

    except Exception as e:
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException(str(e))

