from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QRCodeViewSet, scan_qr_redirect

router = DefaultRouter()
router.register(r'qr-codes', QRCodeViewSet, basename='qrcode')

urlpatterns = [
    path('', include(router.urls)),
    path('qr/<str:model_type>/<int:object_id>/', scan_qr_redirect, name='qr-scan-redirect'),
]
