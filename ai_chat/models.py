from django.db import models
from django.contrib.auth import get_user_model
from tenants.managers import TenantModel

User = get_user_model()


class ChatConversation(TenantModel):
    """
    Conversación de chat con IA
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_conversations',
        verbose_name='Usuario'
    )
    title = models.CharField(
        max_length=200,
        default='Nueva conversación',
        verbose_name='Título'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ai_chat_conversation'
        verbose_name = 'Conversación'
        verbose_name_plural = 'Conversaciones'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class ChatMessage(models.Model):
    """
    Mensaje individual en una conversación
    """
    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('assistant', 'Asistente'),
        ('system', 'Sistema'),
    ]

    conversation = models.ForeignKey(
        ChatConversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Conversación'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        verbose_name='Rol'
    )
    content = models.TextField(verbose_name='Contenido')
    
    # Metadata
    tokens_used = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Tokens usados'
    )
    model_used = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Modelo usado'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_chat_message'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."
