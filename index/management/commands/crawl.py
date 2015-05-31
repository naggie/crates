'''
Crawls a directory for music files and adds to the database.

Optionally removes files after adding them to crates.
'''

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from index.crawler import FileCrawler

class Command(BaseCommand):

    missing_args_message = "Specify <directory> to crawl"

    def add_arguments(self, parser):
        parser.add_argument('directories', nargs='+', type=str)

    def handle(self, *args, **options):

        # TODO external iterator for crawler via generator.
        # TODO ...progress indication here
        for directory in options['directories']:
            crawler = FileCrawler(directory)
            crawler.run_with_progress()



