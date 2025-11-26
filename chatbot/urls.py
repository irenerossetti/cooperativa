from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('api/', views.chatbot_api, name='chatbot_api'),
    path('historial/<str:cliente_id>/', views.get_historial, name='get_historial'),
    path('limpiar/<str:cliente_id>/', views.limpiar_historial, name='limpiar_historial'),
]
