from django.db import models
from tenants.models import Organization

class ChatConversation(models.Model):
    """Modelo para almacenar conversaciones del chatbot"""
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='chat_conversations')
    cliente_id = models.CharField(max_length=255, db_index=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    edad = models.IntegerField(blank=True, null=True)
    tipo_cultivo = models.CharField(max_length=255, blank=True, null=True)
    necesidad_principal = models.CharField(max_length=255, blank=True, null=True)
    fase = models.CharField(max_length=50, default='exploracion')
    tono = models.CharField(max_length=50, default='neutro')
    nivel_interes = models.CharField(max_length=50, default='bajo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chatbot_conversations'
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversación {self.cliente_id} - {self.nombre or 'Anónimo'}"


class ChatMessage(models.Model):
    """Modelo para almacenar mensajes individuales"""
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=[('user', 'Usuario'), ('bot', 'Bot')])
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chatbot_messages'
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.message_type}: {self.content[:50]}"
