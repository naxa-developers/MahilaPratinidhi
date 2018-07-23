import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import District


class Command(BaseCommand):
    help = 'load districts from district_spending.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3], sheet_name="Programme 1").fillna(value=0)
        district = [
            District(
                name=df['Programe Name'][row],


        ) for row in range(1, 78)
        ]
        district = District.objects.bulk_create(district)
        if district:
            self.stdout.write('Successfully loaded districts..')