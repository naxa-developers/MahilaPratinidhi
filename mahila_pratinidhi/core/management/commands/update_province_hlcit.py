import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import ProvinceMahilaPratinidhiForm

class Command(BaseCommand):
    help = 'update hlcit code for pratinidhi shava model'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            total = df['Name_EN'].count()
            for row in range(1, total+1):
                national = ProvinceMahilaPratinidhiForm.objects.filter(
                    name=df['Name_NE'][row],
                    english_name = df['Name_EN'][row],
                    date_of_birth=str(df['Date of Birth_NE'][row])[:10]).update(hlcit_code=df['HLCIT_CODE'][row])
            print("successfully updated hlcit code")

        except Exception as e:
            print(e)

