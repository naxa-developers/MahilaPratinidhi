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


class Province(models.Model):
	name = models.CharField(max_length=300)

	def __str__(self):
		return self.name


class ProvinceMahilaPratinidhiForm(models.Model):
	province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='province_mahila_pratinidhi_form', verbose_name="प्रदेश")
	name = models.CharField(max_length=300, verbose_name="नाम")
	english_name = models.CharField(max_length=300, verbose_name="English Name")
	date_of_birth = models.CharField(max_length=300, verbose_name="जन्ममिती")
	mothers_name = models.CharField(max_length=300, verbose_name="आमाको नाम")
	fathers_name = models.CharField(max_length=300, verbose_name="बाबुको नाम")
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True)
	updated_marital_status = models.CharField(choices=MARITAL_CHOICES, blank=True, max_length=300, verbose_name="बैवाहिक स्थिथि")
	husbands_name = models.CharField(max_length=300, verbose_name="श्रीमानको नाम")
	caste = models.CharField(choices=CASTE_CHOICES, blank=True, max_length=300, verbose_name="जातियता")
	mother_tongue = models.CharField(max_length=300, verbose_name="मातृभाषा", blank=True)
	educational_qualification = models.CharField(max_length=300, verbose_name="औपचारिक शैक्षिक योग्यता", blank=True)
	updated_educational_qualification = models.CharField(choices=EDUCATIONAL_QUALIFICATION_CHOICES, blank=True, max_length=300, verbose_name="शैछिक योग्यता")
	subject = models.CharField(max_length=300, verbose_name="बिषय", blank=True)
	permanent_address = models.CharField(max_length=300, verbose_name="ठेगाना(स्थायी): जिल्ला", blank=True)
	permanent_gapa_napa = models.CharField(max_length=300, verbose_name="गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका", blank=True)
	permanent_ward_no = models.CharField(max_length=300, verbose_name="वडा नं", blank=True)
	permanent_tole = models.CharField(max_length=300, verbose_name="टोल", blank=True)
	temporary_address = models.CharField(max_length=300, verbose_name="ठेगाना(अस्थायी): जिल्ला", blank=True)
	temporary_gapa_napa = models.CharField(max_length=300, verbose_name="गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका", blank=True)
	temporary_ward_no = models.CharField(max_length=300, verbose_name="वडा नं", blank=True)
	temporary_tole = models.CharField(max_length=300, verbose_name="टोल", blank=True)
	mobile = models.CharField(max_length=300, verbose_name="मोवाइल", blank=True)
	contact_number = models.CharField(max_length=300, verbose_name="सम्पर्क न.", blank=True)
	email = models.EmailField(verbose_name="इ-मेल", blank=True)
	social_networking_medium = models.CharField(max_length=300, verbose_name="सामाजिक सन्जालका माध्यम(छ भने):", blank=True)
	nirwachit_prakriya = models.CharField(max_length=300, verbose_name="निर्वाचित प्रक्रिया", blank=True)
	nirwachit_padh = models.CharField(max_length=300, verbose_name="निर्वाचित पद", blank=True)
	pichidiyeko_chhetra_ho_hoina = models.CharField(max_length=300, verbose_name="पिछडिएको क्षेत्र हो कि होइन", blank=True)
	nirwachit_chhetrako_bibaran = models.CharField(max_length=300, verbose_name="निर्वाचित क्षेत्रको विवरण", blank=True)
	nirwachit_vayeko_chhetra_aafno_thegana = models.CharField(max_length=300, verbose_name="निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक", blank=True)
	party_name = models.CharField(max_length=300, verbose_name="पार्टीको विवरण: पार्टीको नाम", blank=True)
	party_joined_date = models.CharField(max_length=300, verbose_name="पार्टीमा संलग्न भएको मिति", blank=True)
	pramukh_jimmewari = models.CharField(max_length=300, verbose_name="प्रमुख जिम्मेवारी ", blank=True)
	nirwachit_chetra_pratiko_pratibadhata = models.TextField(verbose_name="निर्वाचित क्षेत्र प्रतिको प्रतिबध्धता", blank=True)
	aaja_vanda_agadi_chunab_ladnu_vayeko_chha = models.CharField(max_length=300, verbose_name="आज भन्दा अघि चुनाब लड्नुभएको छ?")
	prapta_maat_sankhya = models.CharField(max_length=300, verbose_name="प्राप्त मत संख्या", blank=True)
	samlagna_sang_sastha_samuha = models.CharField(max_length=300, verbose_name="सलग्न संघ, सस्था , समूह", blank=True)
	status = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name="स्थिति")
	image = models.ImageField(blank=True, null=True, upload_to='provinceProfile/', verbose_name="फोटो")

	def __str__(self):
		return "{}-{} फारम".format(self.province.name,self.name)






