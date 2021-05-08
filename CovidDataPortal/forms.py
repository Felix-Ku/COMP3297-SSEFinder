from django import forms
from django.forms import ModelForm, DateField
from django.forms import ModelForm, DateField


class CaseInputForm(forms.Form):
    case_number = forms.IntegerField()
    person_name = forms.CharField()
    id_number = forms.CharField()
    birth_date = DateField(input_formats=['%d-%m-%Y'])
    symptoms_date = DateField(input_formats=['%d-%m-%Y'])
    confirmation_date = DateField(input_formats=['%d-%m-%Y'])

class DateInput(forms.DateInput):
    input_type = "date"

class dateform(forms.Form):
    date_field = forms.DateField(widget=DateInput)

