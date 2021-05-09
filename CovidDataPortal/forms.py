from django import forms
from .models import *


class CaseInputForm(forms.ModelForm):
    class Meta:
        model = case_records
        fields = '__all__'
        widgets = {
            'case_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.TextInput(attrs={'class': 'form-control'}),
            'symptoms_date': forms.TextInput(attrs={'class': 'form-control'}),
            'confirmation_date': forms.TextInput(attrs={'class': 'form-control'}),
        }

class InputForm(forms.ModelForm):
    class Meta:
        model = attendances
        fields = '__all__'
        widgets = {
            'venue_name': forms.NumberInput(attrs={'class': 'form-control'}),
            'venue_location': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'hk_grid': forms.TextInput(attrs={'class': 'form-control'}),
            'event_date': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }


