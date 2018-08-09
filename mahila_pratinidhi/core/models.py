from django.db import models

BOOL_CHOICES = (
	(True, 'पूर्ण'),
	(False, 'अपूर्ण')
	)

MARITAL_CHOICES = (
	('cljjflxt', 'अविवाहित'),
	('ljjflxt', 'विवाहित'),
	('Psn', 'एकल'),
	('cGo', 'अन्य')
	)

EDUCATIONAL_QUALIFICATION_CHOICES = (
										('lg/If/', 'निरक्षर'),
										(';fIf/', 'साक्षर'),
										('P;=Pn=;L= ', 'एस.एल.सी.'),
										('!) @ jf ;f] ;/x', '१० + २ वा सो सरह'),
										(':gfts', 'स्नातक'),
										(':gfsf]]t/', 'स्नाकोतर'),
										('lk=Pr=8L=', 'पि.एच.डी')

									)

CASTE_CHOICES = (
					('blnt', 'दलित'),
					('cflbaf;L÷hghftL', 'आदिबासी / जनजाती'),
					('v; cfo{', 'खस आर्य'),
					('dw];L ', 'मधेसी'),
					('yf?', 'थारु'),
					('d"l:nd', 'मुस्लिम'),
					('cGo', 'अन्य')
				)


class District(models.Model):
	name = models.CharField(max_length=300)
	elected_women = models.IntegerField(default=0)

	def __str__(self):
		return self.name


class MahilaPratinidhiForm(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district', verbose_name="जिल्ला")
	name = models.CharField(max_length=300, verbose_name="नाम")
	age = models.CharField(max_length=300, verbose_name="उमेर", blank=True)
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True)
	updated_marital_status = models.CharField(choices=MARITAL_CHOICES, blank=True, max_length=300, verbose_name="बैवाहिक स्थिथि")
	educational_qualification = models.CharField(max_length=300, verbose_name="शैछिक योग्यता", blank=True)
	updated_educational_qualification = models.CharField(choices=EDUCATIONAL_QUALIFICATION_CHOICES, blank=True, max_length=300, verbose_name="शैछिक योग्यता")
	caste = models.CharField(max_length=300, verbose_name="जातियता", blank=True)
	updated_caste = models.CharField(choices=CASTE_CHOICES, blank=True, max_length=300, verbose_name="जातियता")
	address = models.CharField(max_length=300, verbose_name="ठेगाना", blank=True)
	contact_number = models.CharField(max_length=300, verbose_name="सम्पर्क न.", blank=True)
	email = models.EmailField(verbose_name="इ-मेल", blank=True)
	nirwachit_padh = models.CharField(max_length=300, verbose_name="निर्वाचित पद", blank=True)
	nirwachit_vdc_or_municipality_name = models.CharField(max_length=300, verbose_name="निर्वाचित गा.बि.स वा नगरपालिकाको नाम", blank=True)
	party_name = models.CharField(max_length=300, verbose_name="पार्टीको नाम", blank=True)
	party_joined_date = models.CharField(max_length=300, verbose_name="पार्टीमा संलग्न भएको मिति", blank=True)
	samlagna_sang_sastha_samuha = models.CharField(max_length=300, verbose_name="संलग्न संग सस्था समूह", blank=True)
	nirwachit_chetra_pratiko_pratibadhata = models.TextField(verbose_name="निर्वाचित क्षेत्र प्रतिको प्रतिबध्धता", blank=True)
	status = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name="स्थिति")
	image = models.ImageField(blank=True, upload_to='profile/', verbose_name="फोटो")

	def __str__(self):
		return "{} फारम".format(self.district.name)


