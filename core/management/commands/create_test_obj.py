from django.core.management.base import BaseCommand
from core.tests import create_test_obj

class Command(BaseCommand):
    def handle(self, *args, **options):
        print('=================================================   START | create_test_obj | ')
        create_test_obj(10, 100)
        print('=================================================   FINISH| create_test_obj | ')
