from django import forms
from .models import *


class CaseInputForm(forms.ModelForm):
    class Meta:
        model = cases
        fields = '__all__'
        widgets = {
            'case_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'person_name': forms.TextInput(attrs={'class': 'form-control'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control'}),
            'symptoms_date': forms.DateInput(attrs={'class': 'form-control'}),
            'confirmation_date': forms.DateInput(attrs={'class': 'form-control'}),
        }

