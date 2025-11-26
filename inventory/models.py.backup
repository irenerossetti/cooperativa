from django.db import models
from users.models import User


class InventoryCategory(models.Model):
    """Categorías de inventario"""
    SEED = 'SEED'
    PESTICIDE = 'PESTICIDE'
    FERTILIZER = 'FERTILIZER'
    TOOL = 'TOOL'
    OTHER = 'OTHER'
    
    CATEGORY_CHOICES = [
        (SEED, 'Semilla'),
        (PESTICIDE, 'Pesticida'),
        (FERTILIZER, 'Fertilizante'),
        (TOOL, 'Herramienta'),
        (OTHER, 'Otro'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name='Categoría')
    description = models.TextField(blank=True, verbose_name='Descripción')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'inventory_categories'
        verbose_name = 'Categoría de Inventario'
        verbose_name_plural = 'Categorías de Inventario'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class InventoryItem(models.Model):
    """Items de inventario (semillas, pesticidas, fertilizantes)"""
    # Información básica
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    name = models.CharField(max_length=200, verbose_name='Nombre')
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT,
                                 related_name='items', verbose_name='Categoría')
    
    # Detalles específicos
    species = models.CharField(max_length=200, blank=True, verbose_name='Especie')
    variety = models.CharField(max_length=200, blank=True, verbose_name='Variedad')
    brand = models.CharField(max_length=200, blank=True, verbose_name='Marca')
    
    # Características (para semillas)
    germination_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True,
                                                 verbose_name='Porcentaje de germinación')
    
    # Unidad de medida
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unidad de medida')  # kg, l, unidades
    
    # Stock
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                       verbose_name='Stock actual')
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                       verbose_name='Stock mínimo')
    maximum_stock = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                       verbose_name='Stock máximo')
    
    # Precio
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                     verbose_name='Precio unitario')
    
    # Vencimiento
    expiration_date = models.DateField(null=True, blank=True, verbose_name='Fecha de vencimiento')
    
    # Estado
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    
    # Metadatos
    description = models.TextField(blank=True, verbose_name='Descripción')
    notes = models.TextField(blank=True, verbose_name='Notas')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_items', verbose_name='Creado por')

    class Meta:
        db_table = 'inventory_items'
        verbose_name = 'Item de Inventario'
        verbose_name_plural = 'Items de Inventario'
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def is_low_stock(self):
        """Verifica si el stock está bajo"""
        return self.current_stock <= self.minimum_stock

    @property
    def stock_status(self):
        """Estado del stock"""
        if self.current_stock == 0:
            return 'OUT_OF_STOCK'
        elif self.is_low_stock:
            return 'LOW_STOCK'
        return 'NORMAL'


class InventoryMovement(models.Model):
    """Movimientos de inventario (entradas y salidas)"""
    ENTRY = 'ENTRY'
    EXIT = 'EXIT'
    ADJUSTMENT = 'ADJUSTMENT'
    
    TYPE_CHOICES = [
        (ENTRY, 'Entrada'),
        (EXIT, 'Salida'),
        (ADJUSTMENT, 'Ajuste'),
    ]
    
    # Información básica
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE,
                            related_name='movements', verbose_name='Item')
    movement_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Tipo de movimiento')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Cantidad')
    
    # Detalles
    date = models.DateField(verbose_name='Fecha')
    reference = models.CharField(max_length=200, blank=True, verbose_name='Referencia')
    reason = models.TextField(verbose_name='Motivo')
    
    # Costos
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                    verbose_name='Costo unitario')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                     verbose_name='Costo total')
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='created_movements', verbose_name='Creado por')

    class Meta:
        db_table = 'inventory_movements'
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['item', 'date']),
            models.Index(fields=['movement_type']),
        ]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.item.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        """Actualizar stock al guardar movimiento"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Actualizar stock del item
            if self.movement_type == self.ENTRY:
                self.item.current_stock += self.quantity
            elif self.movement_type == self.EXIT:
                self.item.current_stock -= self.quantity
            elif self.movement_type == self.ADJUSTMENT:
                self.item.current_stock = self.quantity
            
            self.item.save()


class StockAlert(models.Model):
    """Alertas de stock mínimo"""
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE,
                            related_name='alerts', verbose_name='Item')
    alert_date = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de alerta')
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Stock actual')
    minimum_stock = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Stock mínimo')
    is_resolved = models.BooleanField(default=False, verbose_name='Resuelta')
    resolved_date = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de resolución')

    class Meta:
        db_table = 'stock_alerts'
        verbose_name = 'Alerta de Stock'
        verbose_name_plural = 'Alertas de Stock'
        ordering = ['-alert_date']

    def __str__(self):
        return f"Alerta: {self.item.name} - Stock: {self.current_stock}"
