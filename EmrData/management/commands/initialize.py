from django.core.management.base import BaseCommand
from django.core.management import call_command
from oauth2_provider.models import Application


class Command(BaseCommand):

    help = 'Run all other commands uto initialize backend database.'

    def handle(self, *args, **kwargs):

        call_command("")
