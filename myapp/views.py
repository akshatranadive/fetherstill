from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
import os
from datetime import datetime as dt

from .models import Pump, Inflow, Outflow, UploadLog
from .forms import *
import pandas as pd
from myapp.databaseIngest import ingest


def is_admin_or_staff(user):
    return user.is_superuser

def is_atleast_staff(user):
    return user.is_staff

@login_required(login_url="myapp:login_view")
@user_passes_test(is_atleast_staff)
def common_section(request, data_section):
    date_format = '%b. %d, %Y, %I:%M %p'

    if data_section == 'pump':
        data = Pump.objects.all()

        watts_form = WattsFilterForm(request.GET)
        volts_form = VoltsFilterForm(request.GET)
        amp_form = AmperesFilterForm(request.GET)
        flow_form = FlowFilterForm(request.GET)
        temp_form = TempFilterForm(request.GET)
        rate_form = RateFilterForm(request.GET)
        date_form = DateFilterForm(request.GET)

        # Process and apply the filters based on the form data

        filtered_data = data

        if watts_form.is_valid():
            min_w = watts_form.cleaned_data.get('min_w')
            max_w = watts_form.cleaned_data.get('max_w')
            print(min_w)
            if min_w is not None:
                filtered_data = filtered_data.filter(w__gte=min_w)
            if max_w is not None:
                filtered_data = filtered_data.filter(w__lte=max_w)
        if volts_form.is_valid():
            min_v = volts_form.cleaned_data.get('min_v')
            max_v = volts_form.cleaned_data.get('max_v')
            if min_v is not None:
                filtered_data = filtered_data.filter(v__gte=min_v)
            if max_v is not None:
                filtered_data = filtered_data.filter(v__lte=max_v)
        if amp_form.is_valid():
            min_a = amp_form.cleaned_data.get('min_a')
            max_a = amp_form.cleaned_data.get('max_a')
            if min_a is not None:
                filtered_data = filtered_data.filter(a__gte=min_a)
            if max_a is not None:
                filtered_data = filtered_data.filter(a__lte=max_a)
        if flow_form.is_valid():
            min_flow = flow_form.cleaned_data.get('min_flow')
            max_flow = flow_form.cleaned_data.get('max_flow')
            if min_flow is not None:
                filtered_data = filtered_data.filter(flow_l_min__gte=min_flow)
            if max_flow is not None:
                filtered_data = filtered_data.filter(flow_l_min__lte=max_flow)
        if temp_form.is_valid():
            min_temp = temp_form.cleaned_data.get('min_temp')
            max_temp = temp_form.cleaned_data.get('max_temp')
            if min_temp is not None:
                filtered_data = filtered_data.filter(temp_field__gte=min_temp)
            if max_temp is not None:
                filtered_data = filtered_data.filter(temp_field__lte=max_temp)
        if rate_form.is_valid():
            min_rate = rate_form.cleaned_data.get('min_rate')
            max_rate = rate_form.cleaned_data.get('max_rate')
            if min_rate is not None:
                filtered_data = filtered_data.filter(r_sec__gte=min_rate)
            if max_rate is not None:
                filtered_data = filtered_data.filter(r_sec__lte=max_rate)
        if date_form.is_valid():
            min_date = date_form.cleaned_data.get('min_date')
            max_date = date_form.cleaned_data.get('max_date')
            if min_date is not None:
                filtered_data = filtered_data.filter(datetime__gte=min_date)
            if max_date is not None:
                filtered_data = filtered_data.filter(datetime__lte=max_date)

        sort_by = request.GET.get('sort_by', 'w')  # Default to 'iteration' if no column is specified
        sort_order = request.GET.get('sort_order', 'asc')  # Sort order: 'asc' or 'desc'

        order_field = sort_by
        if sort_order == 'desc':
            order_field = '-' + order_field

        # Apply sorting to the filtered data
        sorted_data = filtered_data.order_by(order_field)

        items_per_page = 15

        paginator = Paginator(sorted_data, items_per_page)
        page = request.GET.get('page')

        try:
            pagi_data = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pagi_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page.
            pagi_data = paginator.page(paginator.num_pages)

        return render(request, 'section.html', {
            'data': pagi_data,
            'watts_form': watts_form,
            'volts_form': volts_form,
            'amp_form': amp_form,
            'flow_form': flow_form,
            'temp_form': temp_form,
            'rate_form': rate_form,
            'date_form': date_form,
            'data_section': data_section,
        })
    
    else:
        iteration_form = IterationFilterForm(request.GET)
        cpu_time_form = CpuTimeFilterForm(request.GET)
        travels_form = TravelsFilterForm(request.GET)
        value_form = ValueFilterForm(request.GET)

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

        # Sorting logic
        sort_by = request.GET.get('sort_by', 'iteration')  # Default to 'iteration' if no column is specified
        sort_order = request.GET.get('sort_order', 'asc')  # Sort order: 'asc' or 'desc'

        order_field = sort_by
        if sort_order == 'desc':
            order_field = '-' + order_field


        # Apply sorting to the filtered data
        sorted_data = data.order_by(order_field)

        items_per_page = 15

        paginator = Paginator(sorted_data, items_per_page)
        page = request.GET.get('page')

        try:
            pagi_data = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pagi_data = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g., 9999), deliver last page.
            pagi_data = paginator.page(paginator.num_pages)

        return render(request, 'section.html', {
            'data': pagi_data,  # Pass sorted data to the template
            'iteration_form': iteration_form,
            'cpu_time_form': cpu_time_form,
            'travels_form': travels_form,
            'value_form': value_form,
            'data_section': data_section,
            'sort_order':sort_order
        })


def export_to_csv(request, data_section):
    if data_section == 'pump':
        print("in pump")
        print(data_section)
        data = get_filtered_data(request, data_section)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        # Convert QuerySet to DataFrame
        df = pd.DataFrame(data.values())

        # Select specific columns
        columns = ['w', 'v', 'a', 'flow_l_min', 'r_sec', 'temp_field', 'datetime']
        df = df[columns]

        # Write DataFrame to CSV
        df.to_csv(response, index=False)

    else:
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

    if data_section == 'pump':
        data = get_filtered_data(request, data_section)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

        # Convert QuerySet to DataFrame
        df = pd.DataFrame(data.values())

        # Select specific columns
        columns = ['w', 'v', 'a', 'flow_l_min', 'r_sec', 'temp_field', 'datetime']
        df = df[columns]

        # Write DataFrame to Excel
        df.to_excel(response, index=False)

    else:
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
    if data_section == 'pump':
        data = get_filtered_data(request, data_section)
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="exported_data.json"'

        # Convert QuerySet to DataFrame
        df = pd.DataFrame(data.values())

        # Select specific columns
        columns = ['w', 'v', 'a', 'flow_l_min', 'r_sec', 'temp_field', 'datetime']
        df = df[columns]

        # Write DataFrame to JSON
        response.write(df.to_json(orient='records', indent=2))

    else:
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
    if data_section == 'pump':
        data = Pump.objects.all()

        watts_form = WattsFilterForm(request.GET)
        volts_form = VoltsFilterForm(request.GET)
        amp_form = AmperesFilterForm(request.GET)
        flow_form = FlowFilterForm(request.GET)
        temp_form = TempFilterForm(request.GET)
        rate_form = RateFilterForm(request.GET)
        date_form = DateFilterForm(request.GET)

        # Process and apply the filters based on the form data

        filtered_data = data

        if watts_form.is_valid():
            min_w = watts_form.cleaned_data.get('min_w')
            max_w = watts_form.cleaned_data.get('max_w')
            print(min_w)
            if min_w is not None:
                filtered_data = filtered_data.filter(w__gte=min_w)
            if max_w is not None:
                filtered_data = filtered_data.filter(w__lte=max_w)
        if volts_form.is_valid():
            min_v = volts_form.cleaned_data.get('min_v')
            max_v = volts_form.cleaned_data.get('max_v')
            if min_v is not None:
                filtered_data = filtered_data.filter(v__gte=min_v)
            if max_v is not None:
                filtered_data = filtered_data.filter(v__lte=max_v)
        if amp_form.is_valid():
            min_a = amp_form.cleaned_data.get('min_a')
            max_a = amp_form.cleaned_data.get('max_a')
            if min_a is not None:
                filtered_data = filtered_data.filter(a__gte=min_a)
            if max_a is not None:
                filtered_data = filtered_data.filter(a__lte=max_a)
        if flow_form.is_valid():
            min_flow = flow_form.cleaned_data.get('min_flow')
            max_flow = flow_form.cleaned_data.get('max_flow')
            if min_flow is not None:
                filtered_data = filtered_data.filter(flow_l_min__gte=min_flow)
            if max_flow is not None:
                filtered_data = filtered_data.filter(flow_l_min__lte=max_flow)
        if temp_form.is_valid():
            min_temp = temp_form.cleaned_data.get('min_temp')
            max_temp = temp_form.cleaned_data.get('max_temp')
            if min_temp is not None:
                filtered_data = filtered_data.filter(temp_field__gte=min_temp)
            if max_temp is not None:
                filtered_data = filtered_data.filter(temp_field__lte=max_temp)
        if rate_form.is_valid():
            min_rate = rate_form.cleaned_data.get('min_rate')
            max_rate = rate_form.cleaned_data.get('max_rate')
            if min_rate is not None:
                filtered_data = filtered_data.filter(r_sec__gte=min_rate)
            if max_rate is not None:
                filtered_data = filtered_data.filter(r_sec__lte=max_rate)
        if date_form.is_valid():
            min_date = date_form.cleaned_data.get('min_date')
            max_date = date_form.cleaned_data.get('max_date')
            if min_date is not None:
                filtered_data = filtered_data.filter(datetime__gte=min_date)
            if max_date is not None:
                filtered_data = filtered_data.filter(datetime__lte=max_date)

    else:
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

def logout_view(request):
    logout(request)
    # Optionally, you can redirect the user to a different page after logout
    return redirect('myapp:login_view')  # Replace 'home' with the desired URL name or path


@login_required(login_url="myapp:login_view")
def home_view(request):
    return render(request, 'home.html')



@login_required(login_url="myapp:login_view")
@user_passes_test(is_admin_or_staff)
def upload_view(request):
    context = {}
    if request.method == 'POST':
        print(request.POST, request.FILES)
        form = request.POST
        uploaded_file_category = request.POST["file-category"]
        uploaded_file_type = request.POST["file-type"]
        uploaded_file_date = datetime.strptime(request.POST["file-date"], "%Y-%m-%d")
        uploaded_file = request.FILES["file"]
        file_object = UploadLog.objects.filter(file_category=uploaded_file_category, file_type=uploaded_file_type, file_date=uploaded_file_date)
        name, ext = os.path.splitext(uploaded_file.name)
        date_timestamped_path = "{}\\{}\\{}\\{}{}".format(uploaded_file_date.year,uploaded_file_date.month,uploaded_file_date.day,dt.now().strftime("%Y%d%m%H%M%S%f"),ext)
        upload_file_path = os.path.join(uploaded_file_category,uploaded_file_type,date_timestamped_path)
        if file_object:
            upload_type = "Edited"
            log = UploadLog.objects.create(
                user = request.user,
                upload_type = upload_type,
                file_category = uploaded_file_category,
                file_type = uploaded_file_type,
                file_date = uploaded_file_date,
                file_name = uploaded_file.name,
            )
            log.file.save(upload_file_path, ContentFile(uploaded_file.read()))
            log.save()
            if uploaded_file_type == "Inlet":
                Inflow.objects.filter(date=uploaded_file_date).delete()
            elif uploaded_file_type ==  "Outlet":
                Outflow.objects.filter(date=uploaded_file_date).delete()
            elif uploaded_file_type == "Pump":
                Pump.objects.filter(date=uploaded_file_date).delete()
            else:
                print("Wrong file type!")
        else:
            upload_type = "New"
            log = UploadLog.objects.create(
                user = request.user,
                upload_type = upload_type,
                file_category = uploaded_file_category,
                file_type = uploaded_file_type,
                file_date = uploaded_file_date,
                file_name = uploaded_file.name,
            )
            log.file.save(upload_file_path, ContentFile(uploaded_file.read()))
            log.save()
        ingest(upload_file_path, uploaded_file_type, uploaded_file_date)
        context['name'] = uploaded_file.name
    return render(request, "upload.html", context)