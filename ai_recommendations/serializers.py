from rest_framework import serializers
from .models import (AIRecommendation, AIRecommendationType, PlantingRecommendation,
                     FertilizationPlan, FertilizationApplication, HarvestRecommendation,
                     MarketOpportunity, AILearningData)


class AIRecommendationTypeSerializer(serializers.ModelSerializer):
    name_display = serializers.CharField(source='get_name_display', read_only=True)
    
    class Meta:
        model = AIRecommendationType
        fields = ['id', 'name', 'name_display', 'description', 'is_active']


class PlantingRecommendationSerializer(serializers.ModelSerializer):
    crop_name = serializers.CharField(source='recommended_crop.name', read_only=True)
    
    class Meta:
        model = PlantingRecommendation
        fields = ['id', 'recommended_crop', 'crop_name', 'variety', 'optimal_planting_date',
                  'planting_window_start', 'planting_window_end', 'soil_conditions',
                  'climate_conditions', 'market_demand', 'expected_price', 'estimated_yield',
                  'estimated_harvest_date']


class FertilizationApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizationApplication
        fields = ['id', 'application_number', 'scheduled_date', 'actual_date',
                  'fertilizer_type', 'quantity', 'application_method', 'nutrients',
                  'is_completed', 'notes']


class FertilizationPlanSerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    applications = FertilizationApplicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = FertilizationPlan
        fields = ['id', 'parcel', 'parcel_code', 'campaign', 'campaign_name', 'plan_name',
                  'start_date', 'end_date', 'soil_analysis', 'nutrient_deficiencies',
                  'target_yield', 'is_active', 'applications']


class HarvestRecommendationSerializer(serializers.ModelSerializer):
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    
    class Meta:
        model = HarvestRecommendation
        fields = ['id', 'parcel', 'parcel_code', 'optimal_harvest_date',
                  'harvest_window_start', 'harvest_window_end', 'maturity_level',
                  'weather_conditions', 'market_conditions', 'logistics_readiness',
                  'storage_availability', 'estimated_yield', 'estimated_quality']


class MarketOpportunitySerializer(serializers.ModelSerializer):
    action_display = serializers.CharField(source='get_action_recommended_display', read_only=True)
    
    class Meta:
        model = MarketOpportunity
        fields = ['id', 'product_name', 'current_price', 'predicted_price', 'price_trend',
                  'demand_level', 'demand_trend', 'market_analysis', 'competitors_data',
                  'action_recommended', 'action_display', 'valid_from', 'valid_until']


class AIRecommendationSerializer(serializers.ModelSerializer):
    type_name = serializers.CharField(source='recommendation_type.get_name_display', read_only=True)
    partner_name = serializers.CharField(source='partner.full_name', read_only=True)
    parcel_code = serializers.CharField(source='parcel.code', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    planting_detail = PlantingRecommendationSerializer(read_only=True)
    fertilization_detail = FertilizationPlanSerializer(read_only=True)
    harvest_detail = HarvestRecommendationSerializer(read_only=True)
    market_detail = MarketOpportunitySerializer(read_only=True)
    
    class Meta:
        model = AIRecommendation
        fields = ['id', 'recommendation_type', 'type_name', 'partner', 'partner_name',
                  'parcel', 'parcel_code', 'title', 'description', 'priority', 'priority_display',
                  'confidence_score', 'ai_model_version', 'input_data', 'output_data',
                  'generated_at', 'valid_until', 'is_active', 'was_applied', 'applied_at',
                  'user_rating', 'user_feedback', 'planting_detail', 'fertilization_detail',
                  'harvest_detail', 'market_detail']
        read_only_fields = ['generated_at']


class AILearningDataSerializer(serializers.ModelSerializer):
    recommendation_title = serializers.CharField(source='recommendation.title', read_only=True)
    
    class Meta:
        model = AILearningData
        fields = ['id', 'recommendation', 'recommendation_title', 'actual_outcome',
                  'predicted_outcome', 'accuracy_score', 'error_margin', 'user_satisfaction',
                  'was_successful', 'recorded_at', 'notes']
        read_only_fields = ['recorded_at']
