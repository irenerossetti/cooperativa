from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmActivityViewSet, ActivityTypeViewSet

router = DefaultRouter()
router.register(r'activities', FarmActivityViewSet, basename='farm-activity')
router.register(r'activity-types', ActivityTypeViewSet, basename='activity-type')

urlpatterns = [
    path('', include(router.urls)),
]
