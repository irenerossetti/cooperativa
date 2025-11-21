from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExpenseCategoryViewSet, FieldExpenseViewSet, ParcelProfitabilityViewSet

router = DefaultRouter()
router.register(r'expense-categories', ExpenseCategoryViewSet, basename='expense-category')
router.register(r'expenses', FieldExpenseViewSet, basename='field-expense')
router.register(r'profitability', ParcelProfitabilityViewSet, basename='parcel-profitability')

urlpatterns = [
    path('', include(router.urls)),
]
