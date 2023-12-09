from django.contrib import admin

from myapp.models import Pump, Inflow, Outflow

# Register your models here.

admin.site.register(Pump)
admin.site.register(Inflow)
admin.site.register(Outflow)

