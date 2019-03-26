import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Municipalities, District, Province

class Command(BaseCommand):
    help = 'update district name for municipalities'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            total = df['GaPa'].count()
            for row in range(total):
                province = df['STATE'][row]
                province = 'Province ' + str(province)
                national = District.objects.filter(
                    name=df['DIST'][row],
                ).update(province=Province.objects.get(name=province))
            print('success')
        except Exception as e:
            print('Exception occured', e)
