# urls.py
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('home/', views.home_view, name="home"),
    path('data/<str:data_section>/', views.common_section, name='common_section'),
    path('csv_export/<str:data_section>/', views.export_to_csv, name='csv_export'),
    path('excel_export/<str:data_section>/', views.export_to_excel, name='excel_export'),
    path('json_export/<str:data_section>/', views.export_to_json, name='json_export'),

    # path('battery/', views.battery_view, name='battery'),

]
