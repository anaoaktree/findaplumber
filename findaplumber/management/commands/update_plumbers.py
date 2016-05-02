from django.core.management import BaseCommand
from scraper.models import DjangoCheckATradeScraper


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        sc = DjangoCheckATradeScraper()
        sc()
