# views.py
from django.shortcuts import render
from .models import Pump, Inflow, Outflow
from .forms import DataFilterForm

def common_section(request, data_section):
    data = None
    form = DataFilterForm(request.POST or None)  # Initialize the form with POST data or None

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        start_iteration = form.cleaned_data.get('start_iteration')
        end_iteration = form.cleaned_data.get('end_iteration')

        # Prepare filters based on the provided values
        filters = {}

        # if start_date:
        #     filters['datetime__gte'] = start_date
        # if end_date:
        #     filters['datetime__lte'] = end_date
        if start_iteration:
            filters['iteration__gte'] = start_iteration
        if end_iteration:
            filters['iteration__lte'] = end_iteration

        # Apply filters to the data
        if data_section == 'pump':
            data = Pump.objects.filter(**filters)
        elif data_section == 'inlet':
            data = Inflow.objects.filter(**filters)
        elif data_section == 'outlet':
            data = Outflow.objects.filter(**filters)
    else:
        # No form submission or form is not valid, so display all data
        if data_section == 'pump':
            data = Pump.objects.all()
        elif data_section == 'inlet':
            data = Inflow.objects.all()
        elif data_section == 'outlet':
            data = Outflow.objects.all()

    return render(request, 'section.html', {'data': data, 'data_section': data_section, 'form': form})
