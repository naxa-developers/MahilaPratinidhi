import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import PratinidhiShava

class Command(BaseCommand):
    help = 'load mahila pratinidhi data from munis.csv file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            for row in range(0, df['S.N'].count()):
                national = PratinidhiShava.objects.filter(
                    english_name=df['English Name'][row],
                    age=df['Age'][row],
                    mothers_name=df["Mother's Name"][row],
                    date_of_birth=str(df['Date of BIrth'][row])).update(hlcit_code=df['HLCIT_CODE'][row])
            print("successfully updated hlcit code")

        except Exception as e:
            print('error occured', e)

