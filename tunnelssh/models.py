from django.db import models
from ApiADA.loggers import logging
from datetime import datetime
import django.db.models.options as options
import json
import socket
from django.conf import settings
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('fields_searchable',)
import os
import subprocess
from core.exceptions.customexceptions import ApiException
import time
from core.utils.osutils import OsUtils

log = logging.getLogger(__name__)

# Create your models here.

class Tunnelssh(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False, unique=False)
    host = models.CharField(max_length=255, blank=False, null=False)
    port = models.CharField(max_length=255, blank=False, null=False)
    target_host = models.CharField(max_length=255, blank=False, null=False)
    target_port = models.CharField(max_length=255, blank=False, null=False)
    tunnel_host = models.CharField(max_length=255, blank=True, null=True)
    tunnel_port = models.CharField(max_length=255, blank=True, null=True)
    tunnel_password = models.CharField(max_length=255, blank=False, null=False)
    parent_tunnel = models.ForeignKey('self', null=True, related_name='parent', on_delete=models.CASCADE)
    tunnel_type = models.CharField(max_length=255, blank=False, null=False)
    tunnel_user = models.CharField(max_length=255, blank=False, null=False)
    pid = models.CharField(max_length=255, blank=True, null=True)

    @property
    def isConnected(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            s.connect((self.host, int(self.port)))
            s.shutdown(socket.SHUT_RDWR)
            return True
        except Exception as e:
            return False
        finally:
            s.close()

    def openTunnel(self):
        if (not OsUtils.isWindows):
            raise ApiException('Action not avaliable')

        if (not self.isConnected):
            try:
                log.info('Start:openTunnel')
                plink_options=""
                if (self.tunnel_type == "0" ):
                    plink_options="-batch -v -x -a -T -C -noagent -ssh -L " + str(self.port) + ":" + self.target_host + ":" + str(self.target_port) + " -l " + self.tunnel_user + " -pw " + self.tunnel_password + " " + self.tunnel_host + " -P " + str(self.tunnel_port)
                else:
                    plink_options="-batch -v -x -a -T -C -noagent -ssh -L " + str(self.port) + ":" + self.target_host + ":" + str(self.target_port) + " -l " + self.tunnel_user + " -pw " + self.tunnel_password + " " + self.parent_tunnel.host + " -P " + str(self.parent_tunnel.port.to_s) 
                                    
                cmd=settings.PLINK_COMMAND+ " " + plink_options   

                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008

                p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP)                
                self.pid=p.pid
                self.save()
                '''
                if ((not p) or (not p.stdout)):
                    raise ApiException('Unable to get the stdout')

                output=""
                i=0
                for line in iter(p.stdout.readline, b""):                
                    output=output+line
                    i=i+1
                    if (i>=20):
                        break    
                '''
                log.info('Opening tunnel output')        
                time.sleep(5)
                log.info('End:openTunnel')

            except Exception as e:
                raise ApiException('Error openTunnel %s:' % self.name + str(e))

    
    
    def closeTunnel(self):
        if (not OsUtils.isWindows):
            raise ApiException('Action not avaliable')


        if (self.isConnected):
            try:
                log.info('Start:closeTunnel')
                if (self.pid):
                    #cmd = "wmic process where 'ProcessId=%s' delete" % self.pid
                    cmd = "wmic process where 'ParentProcessId=%s' delete" % self.pid

                    p = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
                    p.wait()
                    
                    output=""
                    i=0
                    for line in iter(p.stdout.readline, b""):                
                        output=output+line
                        i=i+1
                        if (i>=10):
                            break    

                    log.info('Close tunnel output:'+output)                 
                    self.pid=None
                    self.save()
                log.info('End:closeTunnel')
            
            except Exception as e:
                raise ApiException('Error closeTunnel %s:' % self.name + str(e))


    class Meta:
        ordering = ('id',)
        fields_searchable = '__all__'
