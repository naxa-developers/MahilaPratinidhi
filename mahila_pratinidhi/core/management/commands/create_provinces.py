from django.core.management.base import BaseCommand

from core.models import Province, District


class Command(BaseCommand):
    help = 'Create default provinces'

    def handle(self, *args, **options):
        provinces_list = ["Province 1",
                          "Province 2",
                          "Province 3",
                          "Province 4",
                          "Province 5",
                          "Province 6",
                          "Province 7",
                          ]
        for province in provinces_list:
            new_province, created = Province.objects.get_or_create(name=province)
            if created:
                self.stdout.write('Successfully created Provinces .. "%s"' % province)

