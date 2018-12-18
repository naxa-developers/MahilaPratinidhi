from django.core.management.base import BaseCommand

from core.models import Province, District


class Command(BaseCommand):
    help = 'Create default provinces'

    def handle(self, *args, **options):
        district_list = [
            {"Province 1": ["Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", "Okhaldhunga", "Panchthar",
                            "Sankhuwasabha", "Solukhumbu", "Sunsari", "Taplejung", "Terhathum", "Udayapur"]},
            {"Province 2": ["Bara", "Dhanusa", "Mahottari", "Parsa", "Rautahat", "Saptari", "Sarlahi", "Siraha"]},
            {"Province 3": ["Bhaktapur", "Chitwan", "Dhading", "Dolakha", "Kathmandu", "Kavrepalanchowk", "Lalitpur",
                            "Makwanpur", "Nuwakot", "Ramechhap", "Rasuwa", "Sindhuli", "Sindhupalchok"]},
            {"Province 4": ["Baglung", "Gorkha", "Kaski", "Lamjung", "Manang", "Mustang", "Myagdi",
                            "Parbat", "Syangja", "Tanahu", "Nawalparasi East"]},
            {"Province 5": ["Arghakhanchi", "Banke", "Bardiya", "Dang", "Gulmi", "Kapilbastu", "Palpa", "Pyuthan",
                            "Rolpa", "Rukum East", "Rupandehi", "Nawalparasi West"]},
            {"Province 6": ["Dailekh", "Dolpa", "Humla", "Jajarkot", "Jumla", "Kalikot", "Mugu", "Salyan",
                            "Surkhet", "Rukum West"]},
            {"Province 7": ["Achham", "Baitadi", "Bajhang", "Bajura", "Dadeldhura", "Darchula", "Doti", "Kailali",
                            "Kanchanpur"]},

        ]

        for province_district in district_list:
            for province in province_district.keys():
                for district in province_district.values():
                    for district_name in district:
                        # print(district_name)
                        # import ipdb;
                        # ipdb.set_trace()
                        dist = District.objects.get(name=district_name)
                        if dist:
                            District.objects.filter(name=dist).update(province=Province.objects.get(name=province))
