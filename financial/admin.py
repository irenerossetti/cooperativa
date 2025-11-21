from django.contrib import admin
from .models import ExpenseCategory, FieldExpense, ParcelProfitability


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']


@admin.register(FieldExpense)
class FieldExpenseAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'campaign', 'category', 'description', 'total_cost', 'expense_date']
    list_filter = ['category', 'expense_date', 'campaign']
    search_fields = ['description', 'parcel__code']


@admin.register(ParcelProfitability)
class ParcelProfitabilityAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'campaign', 'total_revenue', 'total_expenses', 'gross_profit', 'roi']
    list_filter = ['campaign', 'calculated_at']
    readonly_fields = ['calculated_at']
