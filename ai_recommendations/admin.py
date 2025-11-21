from django.contrib import admin
from .models import (AIRecommendationType, AIRecommendation, PlantingRecommendation,
                     FertilizationPlan, FertilizationApplication, HarvestRecommendation,
                     MarketOpportunity, AILearningData)


@admin.register(AIRecommendationType)
class AIRecommendationTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_filter = ['is_active']


@admin.register(AIRecommendation)
class AIRecommendationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recommendation_type', 'partner', 'priority', 'confidence_score', 'generated_at']
    list_filter = ['recommendation_type', 'priority', 'is_active', 'was_applied']
    search_fields = ['title', 'description']


@admin.register(FertilizationPlan)
class FertilizationPlanAdmin(admin.ModelAdmin):
    list_display = ['plan_name', 'parcel', 'campaign', 'start_date', 'is_active']
    list_filter = ['is_active', 'start_date']


@admin.register(AILearningData)
class AILearningDataAdmin(admin.ModelAdmin):
    list_display = ['recommendation', 'accuracy_score', 'was_successful', 'recorded_at']
    list_filter = ['was_successful', 'recorded_at']
