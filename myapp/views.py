from django.shortcuts import render
from .models import Pump, Inflow, Outflow
from .forms import DataFilterForm, IterationFilterForm, TravelsFilterForm, ValueFilterForm, CpuTimeFilterForm
import pandas as pd

import csv
from django.http import HttpResponse, JsonResponse
import tempfile
import os


def common_section(request, data_section):
   
    iteration_form = IterationFilterForm(request.GET)
    cpu_time_form = CpuTimeFilterForm(request.GET)
    travels_form = TravelsFilterForm(request.GET)
    value_form = ValueFilterForm(request.GET)


    # Sorting logic
    sort_by = request.GET.get('sort_by', 'iteration')  # Default to 'iteration' if no column is specified
    sort_order = request.GET.get('sort_order', 'asc')  # Sort order: 'asc' or 'desc'

    order_field = sort_by
    if sort_order == 'desc':
        order_field = '-' + order_field


    # Process and apply the filters based on the form data

    if data_section == 'pump':
        data = Pump.objects.all()
    elif data_section == 'inlet':
        data = Inflow.objects.all()
    elif data_section == 'outlet':
        data = Outflow.objects.all()

    filtered_data = data

    if iteration_form.is_valid():
        min_iteration = iteration_form.cleaned_data.get('min_iteration')
        max_iteration = iteration_form.cleaned_data.get('max_iteration')
        if min_iteration is not None:
            filtered_data = filtered_data.filter(iteration__gte=min_iteration).order_by(order_field)
        if max_iteration is not None:
            filtered_data = filtered_data.filter(iteration__lte=max_iteration).order_by(order_field)
    if cpu_time_form.is_valid():
        min_cputime = cpu_time_form.cleaned_data.get('min_cputime')
        max_cputime = cpu_time_form.cleaned_data.get('max_cputime')
        if min_cputime is not None:
            filtered_data = filtered_data.filter(cputime__gte=min_cputime).order_by(order_field)
        if max_cputime is not None:
            filtered_data = filtered_data.filter(cputime__lte=max_cputime).order_by(order_field)
    if travels_form.is_valid():
        min_travels = travels_form.cleaned_data.get('min_travels')
        max_travels = travels_form.cleaned_data.get('max_travels')
        if min_travels is not None:
            filtered_data = filtered_data.filter(travels__gte=min_travels).order_by(order_field)
        if max_travels is not None:
            filtered_data = filtered_data.filter(travels__lte=max_travels).order_by(order_field)
    if value_form.is_valid():
        min_value = value_form.cleaned_data.get('min_value')
        max_value = value_form.cleaned_data.get('max_value')
        if min_value is not None:
            filtered_data = filtered_data.filter(value__gte=min_value).order_by(order_field)
        if max_value is not None:
            filtered_data = filtered_data.filter(value__lte=max_value).order_by(order_field)

    return render(request, 'section.html', {
        'data': filtered_data,
        'iteration_form': iteration_form,
        'cpu_time_form': cpu_time_form,
        'travels_form': travels_form,
        'value_form': value_form,
        'data_section': data_section,
    })



    # form = DataFilterForm(request.POST or None)  # Initialize the form with POST data or None
    #
    # if form.is_valid():
    #     start_date = form.cleaned_data.get('start_date')
    #     end_date = form.cleaned_data.get('end_date')
    #     start_iteration = form.cleaned_data.get('start_iteration')
    #     end_iteration = form.cleaned_data.get('end_iteration')
    #
    #     # Prepare filters based on the provided values
    #     filters = {}
    #
    #     # if start_date:
    #     #     filters['datetime__gte'] = start_date
    #     # if end_date:
    #     #     filters['datetime__lte'] = end_date
    #     if start_iteration:
    #         filters['iteration__gte'] = start_iteration
    #     if end_iteration:
    #         filters['iteration__lte'] = end_iteration
    #
    #     # Apply filters to the data
    #     if data_section == 'pump':
    #         data = Pump.objects.filter(**filters).order_by(order_field)
    #     elif data_section == 'inlet':
    #         data = Inflow.objects.filter(**filters).order_by(order_field)
    #     elif data_section == 'outlet':
    #         data = Outflow.objects.filter(**filters).order_by(order_field)
    # else:
    #     # No form submission or form is not valid, so display all data
    #     if data_section == 'pump':
    #         data = Pump.objects.all()
    #     elif data_section == 'inlet':
    #         data = Inflow.objects.all()
    #     elif data_section == 'outlet':
    #         data = Outflow.objects.all()
    #
    # return render(request, 'section.html', {'data': data, 'data_section': data_section, 'form': form})


def export_to_csv(request, data_section):
    data = data_section  # Retrieve the data you want to export, e.g., from the database

    data_list = [
        {
            "iteration": item.iteration,
            "cputime": item.cputime,
            "travels": item.travels,
            "value": item.value,
        }
        for item in data
    ]

    df = pd.DataFrame(data_list)

    df.to_csv("D:/UWindsor/Internship project/Project/fetherstill/my_filename.csv")
    return HttpResponse("<p>Done!</p>")

    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition'] = f'attachment; filename="{data_section}_data.csv"'
    #
    # writer = csv.writer(response)
    #
    # # Write headers to the CSV file
    # writer.writerow(["iteration", "CPU Time", "Travels", "Value"])  # Adjust column headers as needed
    #
    # # Write data rows to the CSV file
    # for item in data:
    #     writer.writerow([item.iteration, item.cputime, item.travels, item.value])
    #
    # return response

    # data_list = [["iteration", "CPU Time", "Travels", "Value"]]  # Headers
    # data_list.extend([[item.iteration, item.cputime, item.travels, item.value] for item in data])
    #
    # return JsonResponse(data_list, safe=False)





