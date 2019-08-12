import os
import subprocess
from core.exceptions.customexceptions import ApiException


class OsUtils:
     
    ##############################################################
    #   Method to verify if the server is running os windows host
    #   inputs:
    #   output:
    #       boolean: 
    #           true - the host is windows
    #           false - the host is not windows    
    ##############################################################
    def isWindows():
        return os.name == 'nt'

    ###########################################################
    #   Method to verify if the process is running
    #   inputs:
    #   output:
    #       boolean: 
    #           true - the process is running
    #           false - the process is not running
    ###########################################################
    def isRunningProcess(pid):
        try:
            if OsUtils.isWindows():
                command='wmic process where "ProcessId = %s" get ProcessId' % pid
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if ((not p) or (not p.stdout)):
                    raise ApiException('Unable to get the stdout')

                for line in p.stdout.readlines():    
                    if "NO INSTANCE" in  line.decode('utf-8').upper():
                        return False
                    elif "PROCESSID" in line.decode('utf-8').upper():
                        return True
                    else:
                        raise ApiException('Unable to verify process running')
            
            else:
                command='ps -p %s' % pid
                p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                exitcode=p.wait()                
                return exitcode == 0

        except Exception as e:
            raise ApiException('Error verifyProcess:' + str(e))




