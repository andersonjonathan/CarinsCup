from django.core.management.base import BaseCommand
from carinscup.models import Result


class Command(BaseCommand):
    help = 'Updates cc points.'

    def handle(self, *args, **options):
        Result.objects.update_cc_points()
