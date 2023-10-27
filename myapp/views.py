# # app_name/views.py
from django.shortcuts import render
from .models import BatteryData
from .models import Pump, Inflow, Outflow
# from .models import PumpData, InletData, OutletData


def battery_view(request):
    data = BatteryData.objects.all()
    return render(request, 'battery.html', {'data': data})

#
# # views.py
# from django.shortcuts import render
# from .models import PumpData, InletData, OutletData
#
# def pump_data(request):
#     data = PumpData.objects.all()
#     return render(request, 'pump_data.html', {'data': data})
#
# def inlet_data(request):
#     data = InletData.objects.all()
#     return render(request, 'inlet_data.html', {'data': data})
#
# def outlet_data(request):
#     data = OutletData.objects.all()
#     return render(request, 'outlet_data.html', {'data': data})

# views.py

def common_section(request, data_section):
    if data_section == 'pump':
        data = Pump.objects.all()
    elif data_section == 'inlet':
        data = Inflow.objects.all()
    elif data_section == 'outlet':
        data = Outflow.objects.all()

    return render(request, 'section.html', {'data': data, 'data_section': data_section})
