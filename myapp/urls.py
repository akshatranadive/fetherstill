# urls.py
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('data/<str:data_section>/', views.common_section, name='common_section'),
    path('exportcsv/<str:data_section>/', views.export_to_csv, name='csv_export'),  # Add this line

    # path('battery/', views.battery_view, name='battery'),

]
