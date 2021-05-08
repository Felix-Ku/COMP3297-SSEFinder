from django import forms

class DateInput(forms.DateInput):
    input_type = "date"

class CaseInputForm(forms.Form):
    case_number = forms.IntegerField()
    person_name = forms.CharField()
    id_number = forms.CharField()
    birth_date = forms.DateField(widget=DateInput)
    symptoms_date = forms.DateField(widget=DateInput)
    confirmation_date = forms.DateField(widget=DateInput)

class dateform(forms.Form):
    date_field = forms.DateField(widget=DateInput)

