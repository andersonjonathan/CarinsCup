from django.core.management.base import BaseCommand
from carinscup.models import Competitor


class Command(BaseCommand):
    help = 'Updates member list.'

    def handle(self, *args, **options):
        Competitor.objects.update_from_eventor()