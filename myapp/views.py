# app_name/views.py
from django.shortcuts import render
from .models import BatteryData

def battery_view(request):
    data = BatteryData.objects.all()
    return render(request, 'battery.html', {'data': data})
