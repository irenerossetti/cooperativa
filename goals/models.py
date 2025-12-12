from django.db import models
from django.contrib.auth import get_user_model
from tenants.managers import TenantModel

User = get_user_model()


class Goal(TenantModel):
    """
    Metas y objetivos de la cooperativa
    """
    TYPE_CHOICES = [
        ('PRODUCTION', 'Producción'),
        ('SALES', 'Ventas'),
        ('QUALITY', 'Calidad'),
        ('EFFICIENCY', 'Eficiencia'),
        ('PARTNERS', 'Socios'),
        ('SURFACE', 'Superficie'),
        ('OTHER', 'Otro'),
    ]
    
    STATUS_CHOICES = [
        ('NOT_STARTED', 'No iniciada'),
        ('IN_PROGRESS', 'En progreso'),
        ('AT_RISK', 'En riesgo'),
        ('COMPLETED', 'Completada'),
        ('CANCELLED', 'Cancelada'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='Tipo'
    )
    
    # Valores
    target_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor objetivo'
    )
    current_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Valor actual'
    )
    unit = models.CharField(
        max_length=50,
        verbose_name='Unidad',
        help_text='Ej: kg, Bs, %, unidades'
    )
    
    # Fechas
    start_date = models.DateField(verbose_name='Fecha de inicio')
    end_date = models.DateField(verbose_name='Fecha de fin')
    
    # Responsable
    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='goals',
        verbose_name='Responsable'
    )
    
    # Estado
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NOT_STARTED',
        verbose_name='Estado'
    )
    
    # Notas
    notes = models.TextField(blank=True, verbose_name='Notas')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goals_goal'
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['type', 'status']),
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f"{self.name} ({self.progress_percentage}%)"

    @property
    def progress_percentage(self):
        """Calcula el porcentaje de progreso"""
        if self.target_value == 0:
            return 0
        progress = (self.current_value / self.target_value) * 100
        return min(round(progress, 2), 100)

    @property
    def is_completed(self):
        """Verifica si la meta está completada"""
        return self.current_value >= self.target_value

    @property
    def is_at_risk(self):
        """Verifica si la meta está en riesgo"""
        from django.utils import timezone
        from datetime import timedelta
        
        if self.is_completed:
            return False
        
        today = timezone.now().date()
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (today - self.start_date).days
        
        if total_days == 0:
            return False
        
        expected_progress = (elapsed_days / total_days) * 100
        actual_progress = self.progress_percentage
        
        # En riesgo si el progreso real es 20% menor al esperado
        return actual_progress < (expected_progress - 20)

    @property
    def days_remaining(self):
        """Calcula los días restantes"""
        from django.utils import timezone
        today = timezone.now().date()
        
        if today > self.end_date:
            return 0
        
        return (self.end_date - today).days

    def update_progress(self, new_value):
        """Actualiza el progreso de la meta"""
        self.current_value = new_value
        
        # Actualizar estado automáticamente
        if self.is_completed:
            self.status = 'COMPLETED'
        elif self.is_at_risk:
            self.status = 'AT_RISK'
        elif self.current_value > 0:
            self.status = 'IN_PROGRESS'
        
        self.save()


class GoalMilestone(models.Model):
    """
    Hitos de una meta
    """
    goal = models.ForeignKey(
        Goal,
        on_delete=models.CASCADE,
        related_name='milestones',
        verbose_name='Meta'
    )
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(blank=True, verbose_name='Descripción')
    target_date = models.DateField(verbose_name='Fecha objetivo')
    completed = models.BooleanField(default=False, verbose_name='Completado')
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Completado en'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'goals_milestone'
        verbose_name = 'Hito'
        verbose_name_plural = 'Hitos'
        ordering = ['target_date']

    def __str__(self):
        return f"{self.title} - {self.goal.name}"

    def mark_completed(self):
        """Marca el hito como completado"""
        from django.utils import timezone
        self.completed = True
        self.completed_at = timezone.now()
        self.save()
