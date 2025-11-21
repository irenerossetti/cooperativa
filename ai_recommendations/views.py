from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from django.utils import timezone
from datetime import date, timedelta
from .models import (AIRecommendation, AIRecommendationType, PlantingRecommendation,
                     FertilizationPlan, FertilizationApplication, HarvestRecommendation,
                     MarketOpportunity, AILearningData)
from .serializers import (AIRecommendationSerializer, AIRecommendationTypeSerializer,
                          FertilizationPlanSerializer, FertilizationApplicationSerializer,
                          AILearningDataSerializer)


class AIRecommendationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIRecommendationType.objects.filter(is_active=True)
    serializer_class = AIRecommendationTypeSerializer
    permission_classes = [IsAuthenticated]


class AIRecommendationViewSet(viewsets.ModelViewSet):
    queryset = AIRecommendation.objects.select_related(
        'recommendation_type', 'partner', 'parcel'
    ).prefetch_related(
        'planting_detail', 'fertilization_detail', 'harvest_detail', 'market_detail'
    )
    serializer_class = AIRecommendationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        partner = self.request.query_params.get('partner')
        parcel = self.request.query_params.get('parcel')
        rec_type = self.request.query_params.get('type')
        is_active = self.request.query_params.get('is_active')
        
        if partner:
            queryset = queryset.filter(partner_id=partner)
        if parcel:
            queryset = queryset.filter(parcel_id=parcel)
        if rec_type:
            queryset = queryset.filter(recommendation_type__name=rec_type)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def generate_planting(self, request):
        """Generar recomendación de siembra con IA"""
        parcel_id = request.data.get('parcel_id')
        
        # Aquí iría la lógica de IA real
        # Por ahora, creamos una recomendación de ejemplo
        
        recommendation = AIRecommendation.objects.create(
            recommendation_type=AIRecommendationType.objects.get(name='PLANTING'),
            parcel_id=parcel_id,
            title="Recomendación de Siembra Generada por IA",
            description="Basado en análisis de mercado y condiciones locales",
            priority='HIGH',
            confidence_score=85.5,
            ai_model_version='v1.0',
            input_data={'parcel_id': parcel_id},
            output_data={'recommendation': 'planting'},
            valid_until=date.today() + timedelta(days=30)
        )
        
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def generate_harvest(self, request):
        """Generar recomendación de cosecha con IA"""
        parcel_id = request.data.get('parcel_id')
        
        recommendation = AIRecommendation.objects.create(
            recommendation_type=AIRecommendationType.objects.get(name='HARVEST'),
            parcel_id=parcel_id,
            title="Momento Óptimo de Cosecha",
            description="Análisis de maduración, clima y mercado",
            priority='HIGH',
            confidence_score=90.0,
            ai_model_version='v1.0',
            valid_until=date.today() + timedelta(days=15)
        )
        
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def generate_market(self, request):
        """Generar oportunidad de mercado con IA"""
        product_name = request.data.get('product_name')
        
        recommendation = AIRecommendation.objects.create(
            recommendation_type=AIRecommendationType.objects.get(name='MARKET'),
            title=f"Oportunidad de Mercado: {product_name}",
            description="Análisis de tendencias de precios y demanda",
            priority='MEDIUM',
            confidence_score=82.0,
            ai_model_version='v1.0',
            valid_until=date.today() + timedelta(days=7)
        )
        
        serializer = self.get_serializer(recommendation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        """Marcar recomendación como aplicada"""
        recommendation = self.get_object()
        recommendation.was_applied = True
        recommendation.applied_at = timezone.now()
        recommendation.save()
        return Response({'message': 'Recomendación marcada como aplicada'})
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Calificar recomendación"""
        recommendation = self.get_object()
        rating = request.data.get('rating')
        feedback = request.data.get('feedback', '')
        
        if not rating or not (1 <= int(rating) <= 5):
            return Response({'error': 'Rating debe ser entre 1 y 5'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        recommendation.user_rating = rating
        recommendation.user_feedback = feedback
        recommendation.save()
        
        return Response({'message': 'Calificación registrada'})


class FertilizationPlanViewSet(viewsets.ModelViewSet):
    queryset = FertilizationPlan.objects.select_related('parcel', 'campaign')
    serializer_class = FertilizationPlanSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def generate_plan(self, request):
        """Generar plan de fertilización con IA"""
        parcel_id = request.data.get('parcel_id')
        campaign_id = request.data.get('campaign_id')
        
        # Crear recomendación base
        recommendation = AIRecommendation.objects.create(
            recommendation_type=AIRecommendationType.objects.get(name='FERTILIZATION'),
            parcel_id=parcel_id,
            title="Plan de Fertilización Personalizado",
            description="Generado por IA basado en análisis de suelo",
            priority='HIGH',
            confidence_score=88.0,
            ai_model_version='v1.0'
        )
        
        # Crear plan de fertilización
        plan = FertilizationPlan.objects.create(
            recommendation=recommendation,
            parcel_id=parcel_id,
            campaign_id=campaign_id,
            plan_name=f"Plan {date.today().year}",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=120),
            soil_analysis={'pH': 6.5, 'N': 'bajo', 'P': 'medio', 'K': 'alto'},
            nutrient_deficiencies=['nitrogen'],
            target_yield=5000
        )
        
        serializer = self.get_serializer(plan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FertilizationApplicationViewSet(viewsets.ModelViewSet):
    queryset = FertilizationApplication.objects.select_related('plan')
    serializer_class = FertilizationApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        """Marcar aplicación como completada"""
        application = self.get_object()
        application.is_completed = True
        application.actual_date = request.data.get('actual_date', date.today())
        application.notes = request.data.get('notes', '')
        application.save()
        return Response({'message': 'Aplicación completada'})


class AILearningDataViewSet(viewsets.ModelViewSet):
    queryset = AILearningData.objects.select_related('recommendation')
    serializer_class = AILearningDataSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def record_outcome(self, request):
        """Registrar resultado real para aprendizaje"""
        recommendation_id = request.data.get('recommendation_id')
        actual_outcome = request.data.get('actual_outcome')
        was_successful = request.data.get('was_successful')
        
        learning_data = AILearningData.objects.create(
            recommendation_id=recommendation_id,
            actual_outcome=actual_outcome,
            predicted_outcome={},
            was_successful=was_successful
        )
        
        serializer = self.get_serializer(learning_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def accuracy_metrics(self, request):
        """Obtener métricas de precisión del modelo"""
        metrics = AILearningData.objects.aggregate(
            avg_accuracy=Avg('accuracy_score'),
            total_predictions=Count('id'),
            successful_predictions=Count('id', filter=models.Q(was_successful=True))
        )
        return Response(metrics)
