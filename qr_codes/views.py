from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from io import BytesIO
import qrcode
import json
from .models import QRCode
from .serializers import QRCodeSerializer


class QRCodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar códigos QR
    """
    permission_classes = [IsAuthenticated]
    serializer_class = QRCodeSerializer
    queryset = QRCode.objects.all()

    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Genera un código QR para un modelo específico
        
        Body:
        {
            "model_type": "partner",
            "object_id": 1,
            "include_data": true  // opcional
        }
        """
        model_type = request.data.get('model_type')
        object_id = request.data.get('object_id')
        include_data = request.data.get('include_data', False)
        
        if not model_type or not object_id:
            return Response(
                {'error': 'model_type y object_id son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verificar que el modelo existe
        model_data = self._get_model_data(model_type, object_id, request)
        if not model_data:
            return Response(
                {'error': f'{model_type} con id {object_id} no encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Crear o actualizar QR
        qr_code, created = QRCode.objects.update_or_create(
            model_type=model_type,
            object_id=object_id,
            defaults={
                'qr_data': json.dumps(model_data) if include_data else f"{model_type}:{object_id}"
            }
        )
        
        # Generar imagen QR
        qr_image_data = self._generate_qr_image(qr_code.qr_data)
        
        serializer = self.get_serializer(qr_code)
        
        return Response({
            'message': 'Código QR generado exitosamente',
            'qr_code': serializer.data,
            'qr_image_base64': qr_image_data,
            'scan_url': f"{request.build_absolute_uri('/')[:-1]}/api/qr-codes/scan/{qr_code.id}/"
        }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def image(self, request, pk=None):
        """Devuelve la imagen del QR como PNG"""
        qr_code = self.get_object()
        
        # Generar imagen
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code.qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return HttpResponse(buffer.getvalue(), content_type='image/png')

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def scan(self, request, pk=None):
        """
        Endpoint público para escanear QR
        Incrementa contador y devuelve datos
        """
        qr_code = self.get_object()
        qr_code.increment_scans()
        
        # Obtener datos actualizados del modelo
        model_data = self._get_model_data(
            qr_code.model_type,
            qr_code.object_id,
            request
        )
        
        return Response({
            'model_type': qr_code.model_type,
            'object_id': qr_code.object_id,
            'data': model_data,
            'scans_count': qr_code.scans_count,
            'last_scanned': qr_code.last_scanned_at
        })

    def _get_model_data(self, model_type, object_id, request):
        """Obtiene datos del modelo según el tipo"""
        try:
            if model_type == 'partner':
                from partners.models import Partner
                obj = Partner.objects.get(id=object_id)
                return {
                    'id': obj.id,
                    'name': obj.full_name,
                    'ci': obj.ci,
                    'phone': obj.phone,
                    'community': obj.community.name if obj.community else None,
                    'status': obj.status
                }
            
            elif model_type == 'parcel':
                from parcels.models import Parcel
                obj = Parcel.objects.get(id=object_id)
                return {
                    'id': obj.id,
                    'code': obj.code,
                    'name': obj.name,
                    'surface': str(obj.surface),
                    'partner': obj.partner.full_name if obj.partner else None,
                    'crop': obj.current_crop.name if obj.current_crop else None,
                    'status': obj.status
                }
            
            elif model_type == 'product':
                from inventory.models import InventoryItem
                obj = InventoryItem.objects.get(id=object_id)
                return {
                    'id': obj.id,
                    'name': obj.name,
                    'code': obj.code,
                    'category': obj.category.name if obj.category else None,
                    'current_stock': obj.current_stock,
                    'unit': obj.unit
                }
            
            elif model_type == 'order':
                from sales.models import Order
                obj = Order.objects.get(id=object_id)
                return {
                    'id': obj.id,
                    'order_number': obj.order_number,
                    'customer': obj.customer.name if obj.customer else None,
                    'total': str(obj.total_amount),
                    'status': obj.status,
                    'date': obj.order_date.isoformat()
                }
            
            elif model_type == 'campaign':
                from campaigns.models import Campaign
                obj = Campaign.objects.get(id=object_id)
                return {
                    'id': obj.id,
                    'name': obj.name,
                    'crop': obj.crop.name if obj.crop else None,
                    'start_date': obj.start_date.isoformat(),
                    'status': obj.status
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting model data: {e}")
            return None

    def _generate_qr_image(self, data):
        """Genera imagen QR y devuelve en base64"""
        import base64
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return base64.b64encode(buffer.getvalue()).decode()


@api_view(['GET'])
@permission_classes([AllowAny])
def scan_qr_redirect(request, model_type, object_id):
    """
    Endpoint público para redireccionar después de escanear QR
    URL: /qr/{model_type}/{object_id}/
    """
    # Buscar o crear QR code
    qr_code, created = QRCode.objects.get_or_create(
        model_type=model_type,
        object_id=object_id,
        defaults={'qr_data': f"{model_type}:{object_id}"}
    )
    
    if not created:
        qr_code.increment_scans()
    
    # Obtener datos
    viewset = QRCodeViewSet()
    model_data = viewset._get_model_data(model_type, object_id, request)
    
    if not model_data:
        return Response(
            {'error': 'Objeto no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({
        'model_type': model_type,
        'object_id': object_id,
        'data': model_data,
        'scans_count': qr_code.scans_count
    })
