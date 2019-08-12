import traceback
import ldap3
import json
from ldap3 import Server, Connection, ALL
from django.conf import settings
from ApiADA.loggers import logging
from core.exceptions.customexceptions import ApiException

log = logging.getLogger(__name__)
 
class VFAuthentication:

    def authenticatVFUser(self, username, password):
        try:
            ldap_server=settings.LDAP_SERVER

            # adjust this to your base dn for searching
            base_dn = settings.LDAP_BASE_DN

            # the following is the user_dn format provided by the ldap server
            user_dn = "uid="+username+","+base_dn
            try:
                conn = Connection(ldap_server, user_dn, password, auto_bind=True)
                search_filter =  "(uid="+username+")"

                try:

                    #if authentication successful, get the full user data
                    conn.search(search_base = base_dn, search_filter = search_filter,search_scope = ldap3.SUBTREE,attributes = ['*'])
                    infoLDAPUser=json.loads(conn.entries[0].entry_to_json())
                    conn.unbind()

                    groups=[]
                    ldap_groups=infoLDAPUser['attributes']['memberOf']
                    for i in range(len(ldap_groups)):
                        if ldap_groups[i].replace('cn=','').replace(',o=airtel.es','') in settings.LDAP_ALLOWED_GROUPS:
                            groups.append(ldap_groups[i].replace('cn=','').replace(',o=airtel.es',''))
                    if len(groups)==0: 
                        raise ApiException('User with invalid privileges.')
                    output={'username':infoLDAPUser['attributes']['uid'][0], 
                            'firstname':infoLDAPUser['attributes']['givenName'][0], 
                            'surname':infoLDAPUser['attributes']['sn'][0],
                            'groups':groups}
                    if ("mail" in infoLDAPUser['attributes']):
                        output['email']=infoLDAPUser['attributes']['mail'][0]        
                    else:
                        output['email']=output['username']+'@unknown.com'            

                    return (output)
                except  Exception as e:
                    conn.unbind()
                    raise ApiException('Authentication Error:' + str(e.args[0]))
            except ldap3.core.exceptions.LDAPBindError as e2:                
                log.error('Exception:'+type(e2).__name__ +" " +str(e2))    
                raise ApiException('Authentication Error:Invalid user or credentials')
            except ldap3.core.exceptions.LDAPSocketOpenError as e3:                
                log.error('Exception:'+type(e3).__name__ +" " +str(e3))    
                raise ApiException('Authentication Error:Unable to connect to LDAP server')
        except Exception as ex:
            log.error('Exception:'+type(ex).__name__ +" " +str(ex))
            log.error(traceback.format_exc())
            raise ApiException(str(ex))

    def mapGroup(self, groupname):
        try:
            map_table=settings.LDAP_MAPPING_GROUPS
            return map_table[groupname]    
        except Exception as e:    
            log.error('Exception:'+type(e).__name__ +" " +str(e))
            log.error(traceback.format_exc())
            raise ApiException('Unable to map group')
            

