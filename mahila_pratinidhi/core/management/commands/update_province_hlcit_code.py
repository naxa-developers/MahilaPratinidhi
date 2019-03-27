import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import ProvinceMahilaPratinidhiForm

class Command(BaseCommand):
    help = 'update any fields of provincialmahilapratinidhiform using this command'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        try:
            for row in range(0, df['S.N'].count()):
                ProvinceMahilaPratinidhiForm.objects.filter(
                    name=df['English Name'][row],
                    age=df['Age'][row]).update(party_name=df['Name of Party'][row])

                ProvinceMahilaPratinidhiForm.objects.filter(
                    name=df['English Name'][row],
                    age=df['Age'][row]).update(nirwachit_chetra_pratiko_pratibadhata=df['Keywords'][row])

                ProvinceMahilaPratinidhiForm.objects.filter(
                    name=df['English Name'][row],
                    age=df['Age'][row]).update(hlcit_code=df['HLCIT_CODE'][row])
            print("successfully updated hlcit code")

        except Exception as e:
            print('error occured', e)