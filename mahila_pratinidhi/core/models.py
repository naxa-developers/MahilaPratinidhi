from django.db import models


class District(models.Model):
	name = models.CharField(max_length=300)


class MahilaPratinidhiForm(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district')
	name = models.CharField(max_length=300, verbose_name="कार्यक्रम")
	age = models.IntegerField()
	marital_status = models.CharField(max_length=300)
	educational_qualification = models.CharField(max_length=300)
	caste = models.CharField(max_length=300)
	address = models.CharField(max_length=300)
	contact_number = models.IntegerField()
	email = models.EmailField()
	nirwachit_padh = models.CharField(max_length=300)
	nirwachit_vdc_or_municipality_name = models.CharField(max_length=300)
	party_name = models.CharField(max_length=300)
	party_joined_date = models.DateField()
	samlagna_sang_sastha_samuha = models.CharField(max_length=300)
	nirwachit_chetra_pratiko_pratibadhata = models.TextField()


class MahilaPratinidhiFile(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='file_district')
	file = models.FileField(upload_to='district/')
