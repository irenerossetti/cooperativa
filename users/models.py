from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class Role(models.Model):
    """Roles del sistema"""
    # Roles predefinidos (opcionales, para referencia)
    ADMIN = 'ADMIN'
    PARTNER = 'PARTNER'
    OPERATOR = 'OPERATOR'
    
    # Ahora name es un CharField libre, sin choices
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre del rol')
    description = models.TextField(blank=True, verbose_name='Descripción')
    permissions = models.JSONField(default=dict, verbose_name='Permisos')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')

    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser):
    """Usuario extendido del sistema"""
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de teléfono debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    phone = models.CharField(max_length=17, validators=[phone_validator], blank=True, verbose_name='Teléfono')
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users', null=True, verbose_name='Rol')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='created_users', verbose_name='Creado por')

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"

    def has_permission(self, permission_key):
        """
        Verifica si el usuario tiene un permiso específico.
        Soporta permisos anidados usando notación de punto.
        
        Ejemplos:
        - 'users.view' -> permissions['users']['view']
        - 'users.delete' -> permissions['users']['delete']
        - 'ui.show_delete_button' -> permissions['ui']['show_delete_button']
        """
        if self.is_superuser:
            return True
        
        if not self.role or not self.role.is_active:
            return False
        
        # Navegar por la estructura anidada usando notación de punto
        keys = permission_key.split('.')
        value = self.role.permissions
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return False
        
        return bool(value)
