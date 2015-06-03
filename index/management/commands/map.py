'''
Proof-of-concept mapper. Symlinks CAS entries to named files.
'''

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from os.path import join,islink
from index.models import AudioFile

from os import unlink

from cas import BasicCAS

# TODO clean file path of unicode stuff

class Command(BaseCommand):

    missing_args_message = "Specify <directory> to map"

    def add_arguments(self, parser):
        parser.add_argument('directories', nargs='+', type=str)

    def handle(self, *args, **options):
        basedir = options['directories'][0]

        cas = BasicCAS()

        for audioFile in AudioFile.objects.all():
            destination = join(basedir, audioFile.map() )

            # probably upgrade or is the same
            if islink(destination): unlink(destination)

            print destination
            cas.link_out(audioFile.ref,destination)

