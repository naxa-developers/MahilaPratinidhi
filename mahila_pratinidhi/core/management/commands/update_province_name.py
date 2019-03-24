from django.core.management.base import BaseCommand

from core.models import Province, District


class Command(BaseCommand):
    help = 'Create default provinces'

    def handle(self, *args, **options):
        Province.objects.filter(name="Province 1").update(name='Province No. 1')
        Province.objects.filter(name="Province 2").update(name='Province No. 2')
        Province.objects.filter(name="Province 3").update(name='Province No. 3')
        Province.objects.filter(name="Province 4").update(name='Gandaki')
        Province.objects.filter(name="Province 5").update(name='Province No. 5')
        Province.objects.filter(name="Province 6").update(name='Karnali')
        Province.objects.filter(name="Province 7").update(name='Sudurpaschim')
        print('Provinces updated')
