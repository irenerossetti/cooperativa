from django.db import models
from tenants.managers import TenantModel


class QRCode(TenantModel):
    """
    Modelo para almacenar códigos QR generados
    """
    MODEL_CHOICES = [
        ('partner', 'Socio'),
        ('parcel', 'Parcela'),
        ('product', 'Producto'),
        ('order', 'Orden'),
        ('campaign', 'Campaña'),
    ]
    
    model_type = models.CharField(
        max_length=20,
        choices=MODEL_CHOICES,
        verbose_name='Tipo de modelo'
    )
    object_id = models.IntegerField(verbose_name='ID del objeto')
    qr_data = models.TextField(verbose_name='Datos del QR')
    qr_image = models.ImageField(
        upload_to='qr_codes/',
        null=True,
        blank=True,
        verbose_name='Imagen QR'
    )
    
    # Metadata
    scans_count = models.IntegerField(default=0, verbose_name='Número de escaneos')
    last_scanned_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Último escaneo'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'qr_codes_qrcode'
        verbose_name = 'Código QR'
        verbose_name_plural = 'Códigos QR'
        unique_together = ['model_type', 'object_id', 'organization']
        indexes = [
            models.Index(fields=['model_type', 'object_id']),
        ]

    def __str__(self):
        return f"QR {self.model_type} #{self.object_id}"

    def increment_scans(self):
        """Incrementa el contador de escaneos"""
        from django.utils import timezone
        self.scans_count += 1
        self.last_scanned_at = timezone.now()
        self.save(update_fields=['scans_count', 'last_scanned_at'])
