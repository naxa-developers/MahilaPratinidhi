import os
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from PIL import Image, ImageOps
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver


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

MOTHER_TONGUE_CHOICES = [
							('नेपाली', 'नेपाली'),
							('मगर खामस्तानाकोतरराजनीति शास्त्र','मगर खामस्तानाकोतरराजनीति शास्त्र'),
							('नेवारी', 'नेवारी'),
							('नेपाल भाषा', 'नेपाल भाषा'),
							('तामाङ', 'तामाङ'),
						]


NIRWACHIT_PRAKRIYA_CHOICES = [
								('समानुपातिक', 'समानुपातिक'),
								('प्रतक्ष्य', 'प्रतक्ष्य'),
							]


NIRWACHIT_PADH_CHOICES = [
							('सांसद - प्रदेशसभा', 'सांसद - प्रदेशसभा'),
						]


PICHIDIYEKO_CHHETRA_CHOICES = [
								('हो', 'हो'),
								('होइन', 'होइन'),
							]


NIRWACHIT_VAYEKO_CHHETRA_AAFNO_THEGANA_VANDA_FARAK_CHOICES = [
													('हो', 'हो'),
													('होइन', 'होइन'),
												]

CHUNAB_LADNU_VAYEKO_CHOICES = [
								('समानुपातिक', 'समानुपातिक'),
								('छैन', 'छैन'),
								('छ', 'छ'),
							]

class CommonShavaFields(models.Model):
	name = models.CharField(max_length=300, verbose_name="नाम")
	english_name = models.CharField(max_length=300, verbose_name="English Name")
	date_of_birth = models.CharField(max_length=300, verbose_name="जन्ममिती")
	age = models.CharField(max_length=300, verbose_name="उमेर", blank=True)
	mothers_name = models.CharField(max_length=300, verbose_name="आमाको नाम")
	fathers_name = models.CharField(max_length=300, verbose_name="बाबुको नाम")
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True, null=True)
	updated_marital_status = models.CharField(choices=MARITAL_CHOICES, max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True, null=True)
	husbands_name = models.CharField(max_length=300, verbose_name="श्रीमानको नाम", blank=True)
	caste = models.CharField(max_length=300, verbose_name="जातियता", blank=True, null=True)
	updated_caste = models.CharField(choices=CASTE_CHOICES, blank=True, max_length=300, verbose_name="जातियता", null=True)
	mother_tongue = models.CharField(max_length=300, verbose_name="मातृभाषा", blank=True, null=True)
	updated_mother_tongue = models.CharField(choices=MOTHER_TONGUE_CHOICES, blank=True, max_length=300, verbose_name="मातृभाषा", null=True)
	educational_qualification = models.CharField(max_length=300, verbose_name="औपचारिक शैक्षिक योग्यता", blank=True, null=True)
	updated_educational_qualification = models.CharField(choices=EDUCATIONAL_QUALIFICATION_CHOICES, blank=True, max_length=300, verbose_name="औपचारिक शैक्षिक योग्यता", null=True)
	subject = models.CharField(max_length=300, verbose_name="बिषय", blank=True, null=True)
	permanent_address = models.CharField(max_length=300, verbose_name="ठेगाना(स्थायी): जिल्ला", blank=True, null=True)
	permanent_gapa_napa = models.CharField(max_length=300, verbose_name="गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका", blank=True, null=True)
	permanent_ward_no = models.CharField(max_length=300, verbose_name="वडा नं", blank=True)
	permanent_tole = models.CharField(max_length=300, verbose_name="टोल", blank=True)
	temporary_address = models.CharField(max_length=300, verbose_name="ठेगाना(अस्थायी): जिल्ला", blank=True)
	temporary_gapa_napa = models.CharField(max_length=300, verbose_name="गाउँपालिका/नगरपालिका/उप-महानगरपालिका/महानगरपालिका", blank=True)
	temporary_ward_no = models.CharField(max_length=300, verbose_name="वडा नं", blank=True)
	temporary_tole = models.CharField(max_length=300, verbose_name="टोल", blank=True)
	mobile = models.CharField(max_length=300, verbose_name="मोवाइल", blank=True)
	contact_number = models.CharField(max_length=300, verbose_name="सम्पर्क न.", blank=True)
	email = models.EmailField(verbose_name="इ-मेल", blank=True, null=True)
	social_networking_medium = models.CharField(max_length=300, verbose_name="सामाजिक सन्जालका माध्यम(छ भने):", blank=True)
	nirwachit_prakriya = models.CharField(max_length=300, verbose_name="निर्वाचित प्रक्रिया", blank=True, null=True)
	updated_nirwachit_prakriya = models.CharField(choices=NIRWACHIT_PRAKRIYA_CHOICES, max_length=300, verbose_name="निर्वाचित प्रक्रिया", blank=True, null=True)
	nirwachit_padh = models.CharField(max_length=300, verbose_name="निर्वाचित पद", blank=True)
	updated_nirwachit_padh = models.CharField(max_length=300, choices=NIRWACHIT_PADH_CHOICES, verbose_name="निर्वाचित पद", blank=True, null=True)
	pichidiyeko_chhetra_ho_hoina = models.CharField(max_length=300, verbose_name="पिछडिएको क्षेत्र हो कि होइन", blank=True, null=True)
	updated_pichidiyeko_chhetra_ho_hoina = models.CharField(choices=PICHIDIYEKO_CHHETRA_CHOICES, max_length=300, verbose_name="पिछडिएको क्षेत्र हो कि होइन", blank=True, null=True)
	nirwachit_chhetrako_bibaran = models.CharField(max_length=300, verbose_name="निर्वाचित क्षेत्रको विवरण", blank=True)
	nirwachit_vayeko_chhetra_aafno_thegana = models.CharField(max_length=300, verbose_name="निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक", blank=True, null=True)
	updated_nirwachit_vayeko_chhetra_aafno_thegana = models.CharField(choices=NIRWACHIT_VAYEKO_CHHETRA_AAFNO_THEGANA_VANDA_FARAK_CHOICES, max_length=300, verbose_name="निर्वाचित भएको क्षेत्र आफ्नो अस्थायी/ स्थायी ठेगाना भन्दा फरक", blank=True, null=True)
	party_name = models.CharField(max_length=300, verbose_name="पार्टीको विवरण: पार्टीको नाम", blank=True)
	party_joined_date = models.CharField(max_length=300, verbose_name="पार्टीमा संलग्न भएको मिति", blank=True, null=True)
	pramukh_jimmewari = models.CharField(max_length=500, verbose_name="प्रमुख जिम्मेवारी ", blank=True)
	nirwachit_chetra_pratiko_pratibadhata = models.TextField(verbose_name="निर्वाचित क्षेत्र प्रतिको प्रतिबध्धता", blank=True, null=True)
	aaja_vanda_agadi_chunab_ladnu_vayeko_chha = models.CharField(max_length=300, verbose_name="आज भन्दा अघि चुनाब लड्नुभएको छ?", blank=True, null=True)
	updated_aaja_vanda_agadi_chunab_ladnu_vayeko_chha = models.CharField(choices=CHUNAB_LADNU_VAYEKO_CHOICES, max_length=300, verbose_name="आज भन्दा अघि चुनाब लड्नुभएको छ?", null=True, blank=True)
	prapta_maat_sankhya = models.CharField(max_length=300, verbose_name="प्राप्त मत संख्या", blank=True)
	samlagna_sang_sastha_samuha = models.CharField(max_length=300, verbose_name="सलग्न संघ, सस्था , समूह", blank=True)
	status = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name="स्थिति")
	image = models.ImageField(blank=True, null=True, upload_to='provinceProfile/', verbose_name="फोटो")
	featured = models.BooleanField(default=False, verbose_name="featured")
	hlcit_code = models.CharField(max_length=20, verbose_name="hlcit_code", null=True)

	class Meta:
		abstract = True

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		super(CommonShavaFields, self).save(force_insert, force_update, *args, **kwargs)
		if self.image:
			image = Image.open(self.image.path)
			# image = image.resize((1350, 700), Image.ANTIALIAS)
			# image.thumbnail((1350, 700), Image.ANTIALIAS)
			image = ImageOps.fit(image, (854, 1062), Image.ANTIALIAS)
			image.save(self.image.path)


class News(models.Model):
	date = models.DateField(blank=False)
	title = models.CharField(max_length=300, blank=False)
	content = models.TextField(blank=False)
	story_headline = models.TextField(blank=True)
	image = models.ImageField(blank=True, upload_to="news/")
	image_credit = models.CharField(blank=True, max_length=300)
	content_type =   models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object=GenericForeignKey('content_type', 'object_id')


	def get_absolute_image_url(self):
		return os.path.join('/media/', self.image.url)

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		super(News, self).save(force_insert, force_update, *args, **kwargs)
		if self.image:
			image = Image.open(self.image.path)
			# image = image.resize((1350, 700), Image.ANTIALIAS)
        	# image.thumbnail((1350, 700), Image.ANTIALIAS)
			image = ImageOps.fit(image, (661, 661), Image.ANTIALIAS)
			image.save(self.image.path)


	def __str__(self):
		return "{}-{} news".format(self.date, self.title)

	class Meta:
		get_latest_by = ['date']



class Province(models.Model):
	name = models.CharField(max_length=300)

	def __str__(self):
		return self.name

class District(models.Model):
	name = models.CharField(max_length=300)
	elected_women = models.IntegerField(default=0)
	province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="प्रदेश", related_name="districts", null=True, blank=True)

	def __str__(self):
		return self.name

class MahilaPratinidhiForm(models.Model):
	MARITAL_CHOICES_local = [("Married","Married"),("Unmarried","Unmarried"),("विवाहित","विवाहित"),("अविवाहित","अविवाहित")]


	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district', verbose_name="जिल्ला")
	name = models.CharField(max_length=300, verbose_name="नाम")
	age = models.CharField(max_length=300, verbose_name="Age", blank=True)
	name_of_elected_region = models.CharField(max_length=300, verbose_name="Name.of.elected.region_NE", blank=True)
	ward = models.CharField(max_length=300, verbose_name="Ward", blank=True)
	marital_status = models.CharField(max_length=300, verbose_name="बैवाहिक स्थिथि", blank=True)
	updated_marital_status = models.CharField(choices=MARITAL_CHOICES_local, blank=True, max_length=300, verbose_name="बैवाहिक स्थिथि")
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
	fathers_name = models.CharField(max_length=300, verbose_name="Father's Name", blank=True)
	mothers_name = models.CharField(max_length=300, verbose_name="Mother's Name", blank=True)
	prapta_maat_sankhya = models.CharField(max_length=300, verbose_name="Votes", blank=True)
	dob = models.CharField(max_length=300, verbose_name="Date of Birth", blank=True)
	status = models.BooleanField(choices=BOOL_CHOICES, default=False, verbose_name="स्थिति")
	image = models.ImageField(blank=True, upload_to='profile/', verbose_name="फोटो")
	featured = models.BooleanField(default=False)
	news = GenericRelation(News)
	province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="प्रदेश", related_name="mahilapratinidhiform", default=1)
	hlcit_code = models.CharField(max_length=20, null=True)


	def __str__(self):
		return "{0} {1} फारम".format(self.name, self.district.name)

	def save(self, force_insert=False, force_update=False, *args, **kwargs):

		super(MahilaPratinidhiForm, self).save(force_insert, force_update, *args, **kwargs)

		if self.image:
			image = Image.open(self.image.path)
    	    # image = image.resize((1350, 700), Image.ANTIALIAS)
    	    # image.thumbnail((1350, 700), Image.ANTIALIAS)
			image = ImageOps.fit(image, (854, 1062), Image.ANTIALIAS)
			image.save(self.image.path)


class ProvinceMahilaPratinidhiForm(CommonShavaFields):
	province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='province_mahila_pratinidhi_form', verbose_name="प्रदेश")
	news = GenericRelation(News)

	def __str__(self):
		return "{}-{} फारम".format(self.province.name, self.name)

class RastriyaShava(CommonShavaFields):
	province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="प्रदेश", default=1)
	samitima_vumika = models.CharField(max_length=300, verbose_name="समितिमा पद", blank=True)
	samlagna_samsadiya_samiti = models.CharField(max_length=300, verbose_name="संलग्न समिति", blank=True)
	news = GenericRelation(News)

	def __str__(self):
		return "{}-{} फारम".format(self.english_name, self.name)

class PratinidhiShava(CommonShavaFields):
	province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name="प्रदेश", default=1)
	samitima_vumika = models.CharField(max_length=300, verbose_name="समितिमा भूमिका", blank=True)
	samlagna_samsadiya_samiti = models.CharField(max_length=300, verbose_name="संलग्न संसदीय समिति", blank=True)
	news = GenericRelation(News)

	def __str__(self):
		return "{}-{} फारम".format(self.english_name, self.name)


class BackgroundImage(models.Model):
	image = models.ImageField(blank=True, upload_to="background/")

	def get_absolute_image_url(self):
		return os.path.join('/media/', self.image.url)

	def save(self, force_insert=False, force_update=False, *args, **kwargs):

		super(BackgroundImage, self).save(force_insert, force_update, *args, **kwargs)

		if self.image:
			image = Image.open(self.image.path)
            # image = image.resize((1350, 700), Image.ANTIALIAS)
            # image.thumbnail((1350, 700), Image.ANTIALIAS)
			image = ImageOps.fit(image, (1920, 1080), Image.ANTIALIAS)

			image.save(self.image.path)

# @receiver(post_init, sender= RastriyaShava)
# def backup_image_path(sender, instance, **kwargs):
#     instance._current_imagen_file = instance.image
#
#
# @receiver(post_save, sender= RastriyaShava)
# def delete_old_image(sender, instance, **kwargs):
#     if hasattr(instance, '_current_imagen_file'):
#         if instance._current_imagen_file != instance.imagen.path:
#             instance._current_imagen_file.delete(save=False)

class DataVizContent(models.Model):
	variable_name = models.CharField(max_length= 50)
	main_content = models.TextField()
	content_variable = models.TextField()
	content_province =models.TextField()
	content_province_vs_federal_vs_national =models.TextField()
	content_party = models.TextField()

	def __str__(self):
		return self.variable_name

class Municipalities(models.Model):
	name= models.CharField(max_length=50)
	district = models.ForeignKey(District,related_name="municipalities",on_delete=models.CASCADE,null=True,blank=True)
	hlcit_code = models.CharField(max_length=50,unique=True)

	def __str__(self):
		return self.name
	

