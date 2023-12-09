# forms.py
from django import forms
from datetime import datetime




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

# Pump filters

class WattsFilterForm(forms.Form):
    min_w = forms.DecimalField(label="Min watt", required=False)
    max_w = forms.DecimalField(label="Max watt", required=False)
class VoltsFilterForm(forms.Form):
    min_v = forms.DecimalField(label="Min voltage", required=False)
    max_v = forms.DecimalField(label="Max voltage", required=False)
class AmperesFilterForm(forms.Form):
    min_a = forms.DecimalField(label="Min ampere", required=False)
    max_a = forms.DecimalField(label="Max ampere", required=False)
class FlowFilterForm(forms.Form):
    min_flow = forms.DecimalField(label="Min flow", required=False)
    max_flow = forms.DecimalField(label="Max flow", required=False)
class TempFilterForm(forms.Form):
    min_temp = forms.DecimalField(label="Min temperature", required=False)
    max_temp = forms.DecimalField(label="Max temperature", required=False)
class RateFilterForm(forms.Form):
    min_rate = forms.DecimalField(label="Min rate", required=False)
    max_rate = forms.DecimalField(label="Max rate", required=False)

class DateFilterForm(forms.Form):
    date_format = '%b. %d, %Y, %I:%M %p'

    min_date = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )
    max_date = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )

    def clean_min_date(self):
        min_date_str = self.cleaned_data.get('min_date')
        if min_date_str:
            return datetime.strptime(min_date_str, self.date_format)
        return None

    def clean_max_date(self):
        max_date_str = self.cleaned_data.get('max_date')
        if max_date_str:
            return datetime.strptime(max_date_str, self.date_format)
        return None


