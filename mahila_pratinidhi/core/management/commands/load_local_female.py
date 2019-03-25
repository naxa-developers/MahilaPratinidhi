import sys
import argparse
import os
from django.core.management.base import BaseCommand

import pandas as pd

from core.models import MahilaPratinidhiForm, District,Municipalities


class Command(BaseCommand):
    help = 'load mahila pratinidhi data from district-wise excel file'

    def add_arguments(self, parser):
        parser.add_argument("-s","--string", type=str, required=True)
        
    
    def handle(self, *args, **options):
        count=0
        for root,dirs,files in os.walk(sys.argv[3]):
            
            for name in files:
                df = pd.read_excel(root + "/"+  name).fillna(value='')
                
                column_name_array = ['Name_EN','Name_NE','Age_EN','Name.of.elected.region_EN','Name.of.elected.region_NE','Ward_EN','Maritial.Status_EN',
                'Maritial.Status_NE','Educational.Background_EN','Educational.Background_NE','Ethnicity_EN','Ethnicity_NE','Email_EN',
                'Elected.Post_EN','Elected.Post_NE',"Name.of.party_EN","Name.of.party_NE","Political.Commitments_EN","Political.Commitments_NE","Father's.Name_EN",
                "Father's.Name_NE","Mother's.Name_EN","Mother's.Name_NE","Number.of.Votes.Received_EN","Date.of.birth_EN",'HLCIT_CODE',"Affiliated.Institutions_NE","Date.of.Affiliation.with.Party_NE","Contact.Number_NE"]

                for xy in column_name_array:
                    if xy not in df.columns:
                        df[xy] = ""
                #import ipdb
                #ipdb.set_trace()
                data=[]
                for row in range(0, len(df.index)):
                    try:
                        try:
                            district_value= Municipalities.objects.get(hlcit_code=df['HLCIT_CODE'][row]).district
                            if district_value is None:
                                district_value = District.objects.get(pk=12)                            
                        except:
                            district_value= District.objects.get(pk=12)
                        
                        try:
                            province_value= Municipalities.objects.get(hlcit_code=df['HLCIT_CODE'][row]).district.province
                            if province_value is None:
                                province_value = District.objects.get(pk=12).province
                        except:
                            province_value = District.objects.get(pk=12).province

                        try:
                            nirwachit = Municipalities.objects.get(hlcit_code=df['HLCIT_CODE'][row])
                        except:
                            nirwachit= Municipalities.objects.get(hlcit_code='524 5 48 3 001')

                            

                        data.append(MahilaPratinidhiForm(
                            #district = District.objects.get(pk=12),
                            district = district_value,
                            province = province_value,
                            nirwachit_vdc_or_municipality_name = nirwachit, 
                            #status = df[""][row],
                            name = df['Name_EN'][row],
                            name_ne_NP= df['Name_NE'][row],
                            name_of_elected_region = df['Name.of.elected.region_EN'][row],
                            name_of_elected_region_ne_NP= df['Name.of.elected.region_NE'][row],
                            ward = df['Ward_EN'][row],
                            marital_status = df['Maritial.Status_EN'][row],
                            marital_status_ne_NP = df['Maritial.Status_NE'][row],
                            updated_marital_status = df['Maritial.Status_EN'][row],
                            updated_marital_status_ne_NP = df['Maritial.Status_NE'][row],
                            educational_qualification = df['Educational.Background_EN'][row],
                            educational_qualification_ne_NP = df['Educational.Background_NE'][row],
                            updated_educational_qualification = df['Educational.Background_EN'][row], 
                            caste = df["Ethnicity_EN"][row],
                            caste_ne_NP = df["Ethnicity_NE"][row],
                            updated_caste = df["Ethnicity_EN"][row],
                            updated_caste_ne_NP = df["Ethnicity_NE"][row],
                            contact_number = df['Contact.Number_NE'][row],
                            email = df["Email_EN"][row],
                            nirwachit_padh = df['Elected.Post_EN'][row],
                            nirwachit_padh_ne_NP = df['Elected.Post_NE'][row],
                            party_name = df["Name.of.party_EN"][row],
                            party_name_ne_NP = df["Name.of.party_NE"][row],
                            party_joined_date = df["Date.of.Affiliation.with.Party_NE"][row],
                            samlagna_sang_sastha_samuha = df["Affiliated.Institutions_NE"][row],
                            nirwachit_chetra_pratiko_pratibadhata = df["Political.Commitments_EN"][row],
                            nirwachit_chetra_pratiko_pratibadhata_ne_NP = df["Political.Commitments_NE"][row], 
                            fathers_name = df["Father's.Name_EN"][row],
                            fathers_name_ne_NP = df["Father's.Name_NE"][row],
                            mothers_name = df["Mother's.Name_EN"][row],
                            mothers_name_ne_NP= df["Mother's.Name_NE"][row],
                            prapta_maat_sankhya = df["Number.of.Votes.Received_EN"][row],
                            dob = df["Date.of.birth_EN"][row],
                            hlcit_code = df['HLCIT_CODE'][row],
                            age= df['Age_EN'][row]
                        ))
                    except Exception as e:
                        print("error in {} {}".format(name,row))
                        print(e)

                    
                data = MahilaPratinidhiForm.objects.bulk_create(data)
                if data:
                    count+=1
                    self.stdout.write('Successfully loaded mahila pratinidhi data..')
                       
                
                    
                    



                
        
    