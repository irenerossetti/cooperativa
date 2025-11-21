from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReportTypeViewSet, ReportViewSet

router = DefaultRouter()
router.register(r'types', ReportTypeViewSet, basename='report-type')
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', include(router.urls)),
]
