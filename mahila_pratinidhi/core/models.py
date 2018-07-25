from django.db import models


class District(models.Model):
	name = models.CharField(max_length=300)

	def __str__(self):
		return self.name


class MahilaPratinidhiForm(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district', verbose_name="जिल्ला")
	name = models.CharField(max_length=300, verbose_name="नाम", blank=True)
	age = models.CharField(max_length=300, verbose_name="उमेर", blank=True)
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True)
	educational_qualification = models.CharField(max_length=300, verbose_name="शैछिक योग्यता", blank=True)
	caste = models.CharField(max_length=300, verbose_name="जातियता", blank=True)
	address = models.CharField(max_length=300, verbose_name="ठेगाना", blank=True)
	contact_number = models.CharField(max_length=300, verbose_name="सम्पर्क न.", blank=True)
	email = models.EmailField(verbose_name="इ-मेल", blank=True)
	nirwachit_padh = models.CharField(max_length=300, verbose_name="निर्वाचित पद", blank=True)
	nirwachit_vdc_or_municipality_name = models.CharField(max_length=300, verbose_name="निर्वाचित गा.बि.स वा नगरपालिकाको नाम", blank=True)
	party_name = models.CharField(max_length=300, verbose_name="पार्टीको नाम", blank=True)
	party_joined_date = models.CharField(max_length=300, verbose_name="पार्टीमा संलग्न भएको मिति", blank=True)
	samlagna_sang_sastha_samuha = models.CharField(max_length=300, verbose_name="संलग्न संग सस्था समूह", blank=True)
	nirwachit_chetra_pratiko_pratibadhata = models.TextField(verbose_name="निर्वाचित क्षेत्र प्रतिको प्रतिबध्धता", blank=True)

	def __str__(self):
		return "{} फारम".format(self.district.name)


