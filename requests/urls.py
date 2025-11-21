from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RequestTypeViewSet, PartnerRequestViewSet

router = DefaultRouter()
router.register(r'request-types', RequestTypeViewSet, basename='request-type')
router.register(r'partner-requests', PartnerRequestViewSet, basename='partner-request')

urlpatterns = [
    path('', include(router.urls)),
]
