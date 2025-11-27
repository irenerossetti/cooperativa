from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'organizations', views.OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_organization, name='register-organization'),
    path('my-organizations/', views.my_organizations, name='my-organizations'),
    
    # Super Admin endpoints
    path('super-admin/stats/', views.super_admin_dashboard_stats, name='super-admin-stats'),
    path('super-admin/organizations/', views.super_admin_list_organizations, name='super-admin-list-orgs'),
    path('super-admin/organizations/create/', views.super_admin_create_organization, name='super-admin-create-org'),
    path('super-admin/organizations/<int:org_id>/', views.super_admin_organization_detail, name='super-admin-org-detail'),
    path('super-admin/organizations/<int:org_id>/update/', views.super_admin_update_organization, name='super-admin-update-org'),
    path('super-admin/organizations/<int:org_id>/delete/', views.super_admin_delete_organization, name='super-admin-delete-org'),
]
