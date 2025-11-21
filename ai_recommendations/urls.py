from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (AIRecommendationViewSet, AIRecommendationTypeViewSet,
                    FertilizationPlanViewSet, FertilizationApplicationViewSet,
                    AILearningDataViewSet)

router = DefaultRouter()
router.register(r'recommendation-types', AIRecommendationTypeViewSet, basename='ai-recommendation-type')
router.register(r'recommendations', AIRecommendationViewSet, basename='ai-recommendation')
router.register(r'fertilization/plans', FertilizationPlanViewSet, basename='fertilization-plan')
router.register(r'fertilization/applications', FertilizationApplicationViewSet, basename='fertilization-application')
router.register(r'learning', AILearningDataViewSet, basename='ai-learning')

urlpatterns = [
    path('', include(router.urls)),
]
