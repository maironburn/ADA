"""
Compress and delete files
Create permissions (read only) to models for a set of groups
"""
# @todo from django.core.management.base import BaseCommand
# @todo from core.ml.SVM.mlSvm_train import MLsvmTrain
# @todo from django.conf import settings
import nltk
import os

# @todo from ApiADA.loggers import logging

log = logging.getLogger(__name__)

# doc
# https://docs.djangoproject.com/en/2.2/howto/custom-management-commands/
#python manage.py closepoll <poll_ids>.
class Command(BaseCommand):
    help = 'Deteccion de averias duplicadas'




    def add_arguments(self, parser):
        parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):

        Command.launchTunnel()

        for poll_id in options['poll_ids']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                raise CommandError('Poll "%s" does not exist' % poll_id)

            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
        exit(0)


    def launchTunnel():
        if (OsUtils.isWindows):
            tunnelsshs=Tunnelssh.objects.all()
            for tunnelssh in tunnelsshs:
                if (not tunnelssh.isConnected):
                    tunnelssh.openTunnel()