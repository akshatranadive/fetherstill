# forms.py
from django import forms

class DataFilterForm(forms.Form):
    # start_date = forms.DateField(label='Start Date')
    # end_date = forms.DateField(label='End Date')
    start_iteration = forms.IntegerField(label='Start Iteration')
    end_iteration = forms.IntegerField(label='End Iteration')


class IterationFilterForm(forms.Form):
    min_iteration = forms.IntegerField(label="Min Iteration", required=False)
    max_iteration = forms.IntegerField(label="Max Iteration", required=False)
class CpuTimeFilterForm(forms.Form):
    min_cputime = forms.IntegerField(label="Min cputime", required=False)
    max_cputime = forms.IntegerField(label="Max cputime", required=False)
class TravelsFilterForm(forms.Form):
    min_travels = forms.DecimalField(label="Min travels", required=False)
    max_travels = forms.DecimalField(label="Max travels", required=False)
class ValueFilterForm(forms.Form):
    min_value = forms.DecimalField(label="Min value", required=False)
    max_value = forms.DecimalField(label="Max value", required=False)
class WattsFilterForm(forms.Form):
    min_w = forms.DecimalField(label="Min value", required=False)
    max_w = forms.DecimalField(label="Max value", required=False)
class VoltsFilterForm(forms.Form):
    min_v = forms.DecimalField(label="Min value", required=False)
    max_v = forms.DecimalField(label="Max value", required=False)
class AmperesFilterForm(forms.Form):
    min_a = forms.DecimalField(label="Min value", required=False)
    max_a = forms.DecimalField(label="Max value", required=False)
class TempFilterForm(forms.Form):
    min_temp = forms.DecimalField(label="Min value", required=False)
    max_temp = forms.DecimalField(label="Max value", required=False)

