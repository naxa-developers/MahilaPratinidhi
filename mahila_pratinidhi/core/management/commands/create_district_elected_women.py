import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import District


class Command(BaseCommand):
    help = 'load district elected women from district wise elected women number xlsx file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3])

        for i in range(0, 77):
            District.objects.filter(name=df['Districts'][i]).update(elected_women=df['Elected'][i])
