from django.core.management.base import BaseCommand
from carinscup.models import Organisation


class Command(BaseCommand):
    help = 'Updates organisation list.'

    def handle(self, *args, **options):
        Organisation.objects.update_from_eventor()
