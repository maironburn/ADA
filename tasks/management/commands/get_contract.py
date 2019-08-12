"""
Create permission groups
Create permissions (read only) to models for a set of groups
"""
from django.conf import settings
from django.core.management.base import BaseCommand
from core.vodafone.smart.contract.models import Contract
from core.vodafone.smart.contr_schedule.models import ContrSchedule
from core.vodafone.smart.site.models import Site
from core.vodafone.smart.contract.serializers import ContractSerializer
from core.vodafone.smart.site.serializers import SiteSerializer

from workflow.models import Workflow


from ApiADA.loggers import logging
log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Get the info for a contract'

    def handle(self, *args, **options):
        log.info('Inicio:'+__name__+"."+self.handle.__name__)
        '''
        contract = Contract.objects.get(objid=452995583)
        contrSchedule = ContrSchedule.objects.get(schedule2contract=contract.objid)
        site = Site.objects.get(objid=contrSchedule.ship_to2site)
        jsonWorkflow = {'contract': ContractSerializer(contract).data , 'site':SiteSerializer(site).data}
        print(jsonWorkflow)
        log.info('Fin:'+__name__+"."+self.handle.__name__)
        '''

        workflow_prueba=Workflow.objects.get(id=1)
        jsonWorkflow = {'contract': ContractSerializer(contract).data , 'site':SiteSerializer(site).data}



