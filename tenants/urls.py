from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_organization, name='register-organization'),
    path('my-organizations/', views.my_organizations, name='my-organizations'),
]
