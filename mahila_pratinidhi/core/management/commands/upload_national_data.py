import sys
import argparse

from django.core.management.base import BaseCommand

import pandas as pd

from core.models import RastriyaShava, Province, District


class Command(BaseCommand):
    help = 'load mahila pratinidhi data from munis.csv file'

    def add_arguments(self, parser):
        parser.add_argument("-f", type=argparse.FileType(), required=True)

    def handle(self, *args, **options):
        df = pd.read_excel(sys.argv[3]).fillna(value='')
        for row in range(0, df['S.N'].count()):
            RastriyaShava.objects.get_or_create(
                province=Province.objects.get(name=df['Province'][row]),
                english_name=df['English Name'][row],
                age=df['Age'][row],
                date_of_birth=df['Date of BIrth'][row],
                mothers_name=df["Mother's Name"][row],
                fathers_name=df["Father's Name"][row],
                marital_status=df['Maritial Status'][row],
                husbands_name=df["Spouse's Name"][row],
                caste=df['Ethnicity'][row],
                mother_tongue=df['Mother Tongue'][row],
                educational_qualification=df['Formal Education'][row],
                subject=df['Degree Name'][row],
                permanent_address=df['Address (Permanent: District)'][row],
                permanent_gapa_napa=df['PVillage / Municipality / Sub-Metropolitan Municipality'][row],
                permanent_ward_no=df['PWard Number'][row],
                permanent_tole=df['PStreet'][row],
                temporary_address=df['Address (Temporary: District)'][row],
                temporary_gapa_napa=df['Village / Municipality / Sub-Metropolitan Municipality'][row],
                temporary_ward_no=df['Ward Number'][row],
                temporary_tole=df['Street'][row],
                mobile=df['Mobile Number'][row],
                contact_number=df['Contact Number'][row],
                email=df['Email'][row],
                social_networking_medium=df['Presence on  Social Media'][row],
                nirwachit_prakriya=df['Election Type'][row],
                nirwachit_padh=df['Elected Post'][row],
                nirwachit_chhetrako_bibaran=df['Description of Elected Area'][row],
                nirwachit_vayeko_chhetra_aafno_thegana=df['Is the elected constituency different than the address of the representative (Yes/No)?'][row],
                party_name=df['Name of Party'][row],
                party_joined_date=df['Date of affiliation with Party'][row],
                pramukh_jimmewari=df['Major responsibility done for the party'][row],
                pichidiyeko_chhetra_ho_hoina=df['Is your area listed in Government of Nepal’s backward area?'][row],
                samlagna_sang_sastha_samuha=df['Details of the recent union, organization, group you are engaged with?'][row],
                nirwachit_chetra_pratiko_pratibadhata=df['Keywords'][row],
                aaja_vanda_agadi_chunab_ladnu_vayeko_chha=df['Have you participated in an election before?'][row])
            print('created')
        self.stdout.write('Successfully loaded mahila pratinidhi data..')
