from django import forms

from .models import MahilaPratinidhiForm


class MahilaPratinidhiFormForm(forms.ModelForm):

	class Meta:
		model = MahilaPratinidhiForm
		exclude = ('district', )

	def __init__(self, *args, **kwargs):
		super(MahilaPratinidhiFormForm, self).__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['age'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		# self.fields['marital_status'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		# self.fields['educational_qualification'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		# self.fields['caste'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['address'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['contact_number'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['nirwachit_padh'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['nirwachit_vdc_or_municipality_name'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px','class': 'form-control'})
		self.fields['party_name'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['party_joined_date'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['samlagna_sang_sastha_samuha'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})
		self.fields['nirwachit_chetra_pratiko_pratibadhata'].widget.attrs.update({'style': 'font-family: preeti; font-size:18px', 'class': 'form-control'})

