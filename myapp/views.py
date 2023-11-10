from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pump, Inflow, Outflow
from .forms import *
import pandas as pd
import json

import csv
from django.http import HttpResponse, JsonResponse
import tempfile
import os

@login_required(login_url="myapp:login_view")
def common_section(request, data_section):
    if data_section == 'pump':
        watts_form = WattsFilterForm(request.GET)
        volts_form = VoltsFilterForm(request.GET)
        amperes_form = AmperesFilterForm(request.GET)
        temp_form = TempFilterForm(request.GET)

        # Sorting logic
        sort_by = request.GET.get('sort_by', 'w')  # Default to 'iteration' if no column is specified
        sort_order = request.GET.get('sort_order', 'asc')  # Sort order: 'asc' or 'desc'

        order_field = sort_by
        if sort_order == 'desc':
            order_field = '-' + order_field

        data = Pump.objects.all()
        
        if watts_form.is_valid():
            min_w = watts_form.cleaned_data.get('min_w')
            max_w = watts_form.cleaned_data.get('max_w')
            if min_w is not None:
                data = data.filter(w__gte=min_w)
            if max_w is not None:
                data = data.filter(w__lte=max_w)

        if volts_form.is_valid():
            min_v = volts_form.cleaned_data.get('min_v')
            max_v = volts_form.cleaned_data.get('max_v')
            if min_v is not None:
                data = data.filter(v__gte=min_v)
            if max_v is not None:
                data = data.filter(v__lte=max_v)

        if amperes_form.is_valid():
            min_a = amperes_form.cleaned_data.get('min_a')
            max_a = amperes_form.cleaned_data.get('max_a')
            if min_a is not None:
                data = data.filter(a__gte=min_a)
            if max_a is not None:
                data = data.filter(a__lte=max_a)

        if temp_form.is_valid():
            min_temp = temp_form.cleaned_data.get('min_temp')
            max_temp = temp_form.cleaned_data.get('max_temp')
            if min_temp is not None:
                data = data.filter(temp__gte=min_temp)
            if max_temp is not None:
                data = data.filter(temp__lte=max_temp)

        sorted_data = data.order_by(order_field)

        return render(request, 'section.html', {
            'data': data,  # Pass sorted data to the template
            'watts_form': watts_form,
            'volts_form': volts_form,
            'amperes_form': amperes_form,
            'temp_form': temp_form,
        })
    
    else:
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
        if data_section == 'inlet':
            data = Inflow.objects.all()
        elif data_section == 'outlet':
            data = Outflow.objects.all()

        if iteration_form.is_valid():
            min_iteration = iteration_form.cleaned_data.get('min_iteration')
            max_iteration = iteration_form.cleaned_data.get('max_iteration')
            if min_iteration is not None:
                data = data.filter(iteration__gte=min_iteration)
            if max_iteration is not None:
                data = data.filter(iteration__lte=max_iteration)

        if cpu_time_form.is_valid():
            min_cputime = cpu_time_form.cleaned_data.get('min_cputime')
            max_cputime = cpu_time_form.cleaned_data.get('max_cputime')
            if min_cputime is not None:
                data = data.filter(cputime__gte=min_cputime)
            if max_cputime is not None:
                data = data.filter(cputime__lte=max_cputime)

        if travels_form.is_valid():
            min_travels = travels_form.cleaned_data.get('min_travels')
            max_travels = travels_form.cleaned_data.get('max_travels')
            if min_travels is not None:
                data = data.filter(travels__gte=min_travels)
            if max_travels is not None:
                data = data.filter(travels__lte=max_travels)

        if value_form.is_valid():
            min_value = value_form.cleaned_data.get('min_value')
            max_value = value_form.cleaned_data.get('max_value')
            if min_value is not None:
                data = data.filter(value__gte=min_value)
            if max_value is not None:
                data = data.filter(value__lte=max_value)

        # Apply sorting to the filtered data
        sorted_data = data.order_by(order_field)

        return render(request, 'section.html', {
            'data': sorted_data,  # Pass sorted data to the template
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
    data = get_filtered_data(request, data_section)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(data.values())

    # Select specific columns
    columns = ['iteration', 'cputime', 'travels', 'value']
    df = df[columns]

    # Write DataFrame to CSV
    df.to_csv(response, index=False)

    return response

def export_to_excel(request, data_section):
    data = get_filtered_data(request, data_section)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(data.values())

    # Select specific columns
    columns = ['iteration', 'cputime', 'travels', 'value']
    df = df[columns]

    # Write DataFrame to Excel
    df.to_excel(response, index=False)

    return response

def export_to_json(request, data_section):
    data = get_filtered_data(request, data_section)
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="exported_data.json"'

    # Convert QuerySet to DataFrame
    df = pd.DataFrame(data.values())

    # Select specific columns
    columns = ['iteration', 'cputime', 'travels', 'value']
    df = df[columns]

    # Write DataFrame to JSON
    response.write(df.to_json(orient='records', indent=2))

    return response

def get_filtered_data(request, data_section):
    iteration_form = IterationFilterForm(request.GET)
    cpu_time_form = CpuTimeFilterForm(request.GET)
    travels_form = TravelsFilterForm(request.GET)
    value_form = ValueFilterForm(request.GET)

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
            filtered_data = filtered_data.filter(iteration__gte=min_iteration)
        if max_iteration is not None:
            filtered_data = filtered_data.filter(iteration__lte=max_iteration)

    if cpu_time_form.is_valid():
        min_cputime = cpu_time_form.cleaned_data.get('min_cputime')
        max_cputime = cpu_time_form.cleaned_data.get('max_cputime')
        if min_cputime is not None:
            filtered_data = filtered_data.filter(cputime__gte=min_cputime)
        if max_cputime is not None:
            filtered_data = filtered_data.filter(cputime__lte=max_cputime)

    if travels_form.is_valid():
        min_travels = travels_form.cleaned_data.get('min_travels')
        max_travels = travels_form.cleaned_data.get('max_travels')
        if min_travels is not None:
            filtered_data = filtered_data.filter(travels__gte=min_travels)
        if max_travels is not None:
            filtered_data = filtered_data.filter(travels__lte=max_travels)

    if value_form.is_valid():
        min_value = value_form.cleaned_data.get('min_value')
        max_value = value_form.cleaned_data.get('max_value')
        if min_value is not None:
            filtered_data = filtered_data.filter(value__gte=min_value)
        if max_value is not None:
            filtered_data = filtered_data.filter(value__lte=max_value)

    return filtered_data

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user  = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('myapp:home')
        else:
            messages.info(request, 'Username or Password is incorrect.')

    context = {}
    return render(request, 'authentication/login_view.html', context)

@login_required(login_url="myapp:login_view")
def home_view(request):
    return render(request, 'home.html')

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





