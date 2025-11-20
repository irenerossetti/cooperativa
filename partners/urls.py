from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PartnerViewSet, CommunityViewSet

router = DefaultRouter()
router.register(r'partners', PartnerViewSet, basename='partner')
router.register(r'communities', CommunityViewSet, basename='community')

urlpatterns = [
    path('', include(router.urls)),
]
