from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatConversationViewSet, quick_question

router = DefaultRouter()
router.register(r'conversations', ChatConversationViewSet, basename='chat-conversation')

urlpatterns = [
    path('', include(router.urls)),
    path('quick/', quick_question, name='quick-question'),
]
