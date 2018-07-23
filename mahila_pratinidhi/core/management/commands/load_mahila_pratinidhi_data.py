import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import MahilaPratinidhiForm, District


class Command(BaseCommand):
    help = 'load mahila pratinidhi data from munis.csv file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        data = [
            MahilaPratinidhiForm(
				district = District.objects.get(id=154),
                name=df['gfd'][row],
				age=df['pd]/'][row],
				marital_status=df['j}jflxs l:lYft'][row],
				educational_qualification=df['z}lIfs of]Uotf'][row],
				caste=df['hfltotf'][row],
				address=df['7]ufgf'][row],
				contact_number=df[';Dks{ g '][row],
				email=df['Od]n 7]ufgf'][row],
				nirwachit_padh=df['lgjf{lrt kb'][row],
				nirwachit_vdc_or_municipality_name=df['lgjf{lrt uf lj ; tyf gu/kflnsfsf]] gfd '][row],
				party_name=df['kf6L{sf] gfd '][row],
				party_joined_date=df['kf6L{df ;++++nUg ePsf] ldtL'][row],
				samlagna_sang_sastha_samuha=df[' ;++++nUg ;++3 ;F:yf ;d"x  '][row],
				nirwachit_chetra_pratiko_pratibadhata=df['lgjf{lrt Ifq k||ltsf] k|ltaM4tf '][row],

			) for row in range(0, 93)
        ]
        data = MahilaPratinidhiForm.objects.bulk_create(data)
        if data:
            self.stdout.write('Successfully loaded mahila pratinidhi data..')