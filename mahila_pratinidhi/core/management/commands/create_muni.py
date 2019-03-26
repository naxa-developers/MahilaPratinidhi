import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Municipalities


class Command(BaseCommand):
    help = 'load municipalities from hlcit_excel.xlsx file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
       
        df = pd.read_excel(sys.argv[3], sheet_name="hlcit_excel")
        muni = [
            Municipalities(
                name=df['LU_Name'][row],
                hlcit_code=df['HLCIT_CODE'][row]


        )for row in range(0, 775)
        ]
        muni = Municipalities.objects.bulk_create(muni)
        if muni:
            self.stdout.write('Successfully loaded municipalities..')