import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import Municipalities,District 

class Command(BaseCommand):
    help = 'update district name for municipalities'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            total = df['GaPa'].count()
            #import ipdb
            #ipdb.set_trace()
            for row in range(total):
                print(df['DIST'][row])
                national = Municipalities.objects.filter(
                    name=df['GaPa'][row],
                    ).update(district=District.objects.get(name=str(df['DIST'][row])))
            print("successfully updated")
        except Exception as e:
            print(e)

