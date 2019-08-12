from django.core.management.base import BaseCommand
from core.beans.analysis_averia.analysis_averia import AnalysisAveria
import os
import traceback
from auditprocess.models import Auditprocess
from core.utils.osutils import OsUtils
from tunnelssh.models import Tunnelssh

from ApiADA.loggers import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'batch process to get the backlog incremental'

    def handle(self, *args, **options):
        log.info('Start:'+__name__+"."+self.handle.__name__)

        Command.launchTunnel()

        auditprocess=Auditprocess()
        try:
          
            current_pid=str(os.getpid())
            auditprocess.setInitial({"process": Auditprocess.PROCESS_INCREMENTAL, "pid": current_pid})

            auditoriaProcesses=Auditprocess.objects.filter(end_date=None, process=Auditprocess.PROCESS_INCREMENTAL).all()
            for audit in auditoriaProcesses:
                if ((audit.pid) and (audit.pid!=current_pid) and (OsUtils.isRunningProcess(audit.pid))):
                    auditprocess.setCancelled({"msg":"Another instance %s is running" % audit.pid})
                    log.info('End:'+__name__+"."+self.handle.__name__+" exit code:-1")
                    exit(-1)
                elif ((audit.pid) and (audit.pid!=current_pid) and (not OsUtils.isRunningProcess(audit.pid))):
                    audit.setCancelled({"msg":"Instance %s is not running" % audit.pid})

                     

            AnalysisAveria.analyzeBacklog(None, auditprocess)
            
            log.info('End:'+__name__+"."+self.handle.__name__+" exit code:0")
            exit(0)

        except Exception as e:
           auditprocess.setError({"msg":str(e)})
           log.error ("Error to analyze the backlog incremental. "+ str(e))
           log.error(traceback.format_exc())
           log.info('End:'+__name__+"."+self.handle.__name__+" exit code:-1")
           exit(-1)


    def launchTunnel():
        if (OsUtils.isWindows):
            tunnelsshs=Tunnelssh.objects.all()
            for tunnelssh in tunnelsshs:
                if (not tunnelssh.isConnected):
                    tunnelssh.openTunnel()

