# app_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('battery/', views.battery_view, name='battery'),
]
