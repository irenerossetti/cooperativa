from django.urls import path
from .views import dashboard_metrics, dashboard_summary, dashboard_charts, realtime_dashboard

urlpatterns = [
    path('metrics/', dashboard_metrics, name='dashboard-metrics'),
    path('summary/', dashboard_summary, name='dashboard-summary'),
    path('charts/', dashboard_charts, name='dashboard-charts'),
    path('realtime/', realtime_dashboard, name='dashboard-realtime'),
]
