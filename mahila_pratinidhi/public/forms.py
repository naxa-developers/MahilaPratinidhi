from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from core.models import *
# from dal import autocomplete


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# class PersonForm(forms.ModelForm):
#     class Meta:
#         model = RastriyaShava
#         fields = ('__all__')
#         widgets = {'english_name': autocomplete.ModelSelect2(url='name_autocomplete')}