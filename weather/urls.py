from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('current/', views.get_current_weather, name='current'),
    path('forecast/', views.get_forecast, name='forecast'),
    path('agricultural/', views.get_agricultural_data, name='agricultural'),
    path('parcel/<int:parcel_id>/', views.get_weather_by_parcel, name='by_parcel'),
]
