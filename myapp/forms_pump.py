# forms.py
from django import forms

class DataFilterForm(forms.Form):
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')
    start_iteration = forms.IntegerField(label='Start Iteration')
    end_iteration = forms.IntegerField(label='End Iteration')
