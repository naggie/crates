'''
Crawls a directory for music files and adds to the database.

Optionally removes files after adding them to crates.
'''

from os import unlink
from os.path import abspath

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    pass
