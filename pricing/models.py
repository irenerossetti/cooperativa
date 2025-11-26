from django.db import models
from django.core.validators import MinValueValidator
from campaigns.models import Campaign
from production.models import HarvestedProduct
from users.models import User
from tenants.managers import TenantModel


class PriceList(TenantModel):
    """Listas de precios por campaña/temporada"""
    # Información básica
    name = models.CharField(max_length=200, verbose_name='Nombre')
    code = models.CharField(max_length=50, verbose_name='Código')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='price_lists',
                                 verbose_name='Campaña')
    
    # Vigencia
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin')
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    
    # Descripción
    description = models.TextField(blank=True, verbose_name='Descripción')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_price_lists', verbose_name='Creado por')

    class Meta:
        db_table = 'price_lists'
        verbose_name = 'Lista de Precios'
        verbose_name_plural = 'Listas de Precios'
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['campaign', 'is_active']),
        ]

    class Meta:
        unique_together = [
            ['organization', 'code'],
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def is_valid_for_date(self, date):
        """Verifica si la lista está vigente para una fecha"""
        return self.is_active and self.start_date <= date <= self.end_date


class PriceListItem(TenantModel):
    """Items de lista de precios"""
    price_list = models.ForeignKey(PriceList, on_delete=models.CASCADE,
                                   related_name='items', verbose_name='Lista de precios')
    product_name = models.CharField(max_length=200, verbose_name='Nombre del producto')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,
                                     validators=[MinValueValidator(0)], verbose_name='Precio unitario')
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidad de medida')
    
    # Descuentos por volumen (opcional)
    min_quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name='Cantidad mínima')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0,
                                             validators=[MinValueValidator(0)],
                                             verbose_name='Descuento (%)')
    
    # Metadatos
    notes = models.TextField(blank=True, verbose_name='Notas')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        db_table = 'price_list_items'
        verbose_name = 'Item de Lista de Precios'
        verbose_name_plural = 'Items de Listas de Precios'
        ordering = ['product_name']

    def __str__(self):
        return f"{self.price_list.code} - {self.product_name}"

    def get_price_for_quantity(self, quantity):
        """Obtiene el precio considerando descuentos por volumen"""
        if self.min_quantity and quantity >= self.min_quantity:
            discount = (self.unit_price * self.discount_percentage) / 100
            return self.unit_price - discount
        return self.unit_price
