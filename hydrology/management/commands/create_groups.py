#Create permission groups

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

GROUPS = ['observers' , 'engineers',]

class Command(BaseCommand):
    help = 'creates groups'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)

