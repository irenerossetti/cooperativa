from rest_framework import serializers
from .models import RequestType, PartnerRequest, RequestItem, RequestAttachment


class RequestTypeSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = RequestType
        fields = ['id', 'name', 'name_display', 'description', 'is_active']


class RequestItemSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    
    class Meta:
        model = RequestItem
        fields = ['id', 'item', 'item_name', 'quantity', 'approved_quantity', 'notes']


class RequestAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestAttachment
        fields = ['id', 'file', 'file_name', 'file_type', 'description', 'uploaded_at']


class PartnerRequestSerializer(serializers.ModelSerializer):
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    request_type_name = serializers.CharField(source='request_type.get_name_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    request_items = RequestItemSerializer(many=True, read_only=True)
    attachments = RequestAttachmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = PartnerRequest
        fields = ['id', 'request_number', 'partner', 'partner_name', 'request_type', 
                  'request_type_name', 'title', 'description', 'priority', 'request_date',
                  'required_date', 'status', 'status_display', 'assigned_to', 'assigned_to_name',
                  'response', 'response_date', 'request_items', 'attachments', 'notes']
        read_only_fields = ['request_date', 'response_date']

    def validate_request_number(self, value):
        request_id = self.instance.id if self.instance else None
        if PartnerRequest.objects.filter(request_number=value).exclude(id=request_id).exists():
            raise serializers.ValidationError("Este número de solicitud ya existe.")
        return value
