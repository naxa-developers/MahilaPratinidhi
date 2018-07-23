from django.db import models


class District(models.Model):
	name = models.CharField(max_length=300)

	def __str__(self):
		return self.name


class MahilaPratinidhiForm(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district', verbose_name="जिल्ला")
	name = models.CharField(max_length=300, verbose_name="नाम")
	age = models.CharField(max_length=300, verbose_name="उमेर")
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि")
	educational_qualification = models.CharField(max_length=300, verbose_name="शैछिक योग्यता")
	caste = models.CharField(max_length=300, verbose_name="जातियता")
	address = models.CharField(max_length=300, verbose_name="ठेगाना")
	contact_number = models.CharField(max_length=300, verbose_name="सम्पर्क न.")
	email = models.EmailField(verbose_name="इ-मेल")
	nirwachit_padh = models.CharField(max_length=300, verbose_name="निर्वाचित पद")
	nirwachit_vdc_or_municipality_name = models.CharField(max_length=300, verbose_name="निर्वाचित गा.बि.स वा नगरपालिकाको नाम")
	party_name = models.CharField(max_length=300, verbose_name="पार्टीको नाम")
	party_joined_date = models.CharField(max_length=300, verbose_name="पार्टीमा संलग्न भएको मिति")
	samlagna_sang_sastha_samuha = models.CharField(max_length=300, verbose_name="संलग्न संग सस्था समूह")
	nirwachit_chetra_pratiko_pratibadhata = models.TextField(verbose_name="निर्वाचित क्षेत्र प्रतिको प्रतिबध्धता")

	def __str__(self):
		return "{} फारम".format(self.district.name)


