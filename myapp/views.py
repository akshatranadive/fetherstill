from django.shortcuts import render
from .models import Pump, Inflow, Outflow
from .forms import DataFilterForm

def common_section(request, data_section):
    data = None
    form = DataFilterForm(request.POST or None)  # Initialize the form with POST data or None

    # Sorting logic
    sort_by = request.GET.get('sort_by', 'iteration')  # Default to 'iteration' if no column is specified
    sort_order = request.GET.get('sort_order', 'asc')  # Sort order: 'asc' or 'desc'

    order_field = sort_by
    if sort_order == 'desc':
        order_field = '-' + order_field

    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        start_iteration = form.cleaned_data.get('start_iteration')
        end_iteration = form.cleaned_data.get('end_iteration')

        # Prepare filters based on the provided values
        filters = {}
        if start_iteration:
            filters['iteration__gte'] = start_iteration
        if end_iteration:
            filters['iteration__lte'] = end_iteration

        # Apply filters to the data
        if data_section == 'pump':
            data = Pump.objects.filter(**filters).order_by(order_field)
        elif data_section == 'inlet':
            data = Inflow.objects.filter(**filters).order_by(order_field)
        elif data_section == 'outlet':
            data = Outflow.objects.filter(**filters).order_by(order_field)
    else:
        # No form submission or form is not valid, so display all data
        if data_section == 'pump':
            data = Pump.objects.all().order_by(order_field)
        elif data_section == 'inlet':
            data = Inflow.objects.all().order_by(order_field)
        elif data_section == 'outlet':
            data = Outflow.objects.all().order_by(order_field)

    return render(request, 'section.html', {'data': data, 'data_section': data_section, 'form': form})
