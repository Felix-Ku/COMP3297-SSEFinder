from django import forms

class DateInput(forms.DateInput):
    input_type = "date"

class CaseInputForm(forms.Form):
    case_number = forms.IntegerField()
    person_name = forms.CharField()
    id_number = forms.CharField()
    birth_date = forms.DateTimeField(widget=DateInput)
    symptoms_date = forms.DateTimeField(widget=DateInput)
    confirmation_date = forms.DateTimeField(widget=DateInput)

class dateform(forms.Form):
    date_field = forms.DateField(widget=DateInput)

