"""
URL configuration for project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Sprint 1
    path('api/auth/', include('users.urls')),
    path('api/partners/', include('partners.urls')),
    path('api/parcels/', include('parcels.urls')),
    path('api/audit/', include('audit.urls')),
    # Sprint 2
    path('api/campaigns/', include('campaigns.urls')),
    path('api/farm-activities/', include('farm_activities.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/production/', include('production.urls')),
    # Sprint 3
    path('api/sales/', include('sales.urls')),
    path('api/requests/', include('requests.urls')),
    path('api/pricing/', include('pricing.urls')),
    path('api/shipping/', include('shipping.urls')),
    # Sprint 4
    path('api/ai/', include('ai_recommendations.urls')),
    path('api/financial/', include('financial.urls')),
    path('api/reports/', include('reports.urls')),
    path('api/traceability/', include('traceability.urls')),
    path('api/analytics/', include('analytics.urls')),
    # Sprint 5 - Completar casos de uso
    path('api/monitoring/', include('monitoring.urls')),
    path('api/weather/', include('weather.urls')),
]
