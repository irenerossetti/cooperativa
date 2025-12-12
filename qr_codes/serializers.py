from rest_framework import serializers
from .models import QRCode


class QRCodeSerializer(serializers.ModelSerializer):
    """Serializer para códigos QR"""
    
    model_type_display = serializers.CharField(
        source='get_model_type_display',
        read_only=True
    )
    
    class Meta:
        model = QRCode
        fields = [
            'id', 'model_type', 'model_type_display', 'object_id',
            'qr_data', 'qr_image', 'scans_count', 'last_scanned_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'scans_count', 'last_scanned_at', 'created_at', 'updated_at']
