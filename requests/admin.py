from django.contrib import admin
from .models import RequestType, PartnerRequest, RequestItem, RequestAttachment


@admin.register(RequestType)
class RequestTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']


class RequestItemInline(admin.TabularInline):
    model = RequestItem
    extra = 1


@admin.register(PartnerRequest)
class PartnerRequestAdmin(admin.ModelAdmin):
    list_display = ['request_number', 'partner', 'request_type', 'priority', 'status', 'request_date']
    list_filter = ['status', 'priority', 'request_type', 'request_date']
    search_fields = ['request_number', 'title', 'partner__first_name', 'partner__last_name']
    inlines = [RequestItemInline]


@admin.register(RequestAttachment)
class RequestAttachmentAdmin(admin.ModelAdmin):
    list_display = ['request', 'file_name', 'uploaded_at']
    list_filter = ['uploaded_at']
