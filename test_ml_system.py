"""
Script de prueba para el sistema de ML
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reports.ml_predictions import YieldPredictor, ProductionForecaster
from parcels.models import Parcel
from partners.models import Partner

print("=" * 60)
print("PRUEBA DEL SISTEMA DE MACHINE LEARNING")
print("=" * 60)

# 1. Verificar datos disponibles
print("\n1. Verificando datos disponibles...")
parcels_count = Parcel.objects.count()
partners_count = Partner.objects.count()
print(f"   ✓ Parcelas en BD: {parcels_count}")
print(f"   ✓ Socios en BD: {partners_count}")

if parcels_count < 10:
    print("\n   ⚠️  ADVERTENCIA: Se necesitan al menos 10 parcelas con producción")
    print("      para entrenar el modelo correctamente.")

# 2. Entrenar el modelo
print("\n2. Entrenando modelo Random Forest...")
predictor = YieldPredictor()
result = predictor.train()

if result['success']:
    print(f"   ✓ Modelo entrenado exitosamente!")
    print(f"   - Muestras utilizadas: {result['samples']}")
    print(f"   - Precisión en entrenamiento: {result['train_score']:.2%}")
    print(f"   - Precisión en prueba: {result['test_score']:.2%}")
else:
    print(f"   ✗ Error: {result['message']}")
    exit(1)

# 3. Obtener importancia de features
print("\n3. Analizando importancia de factores...")
importance = predictor.get_feature_importance()
print(f"   - Superficie: {importance['surface']:.2%}")
print(f"   - Tipo de suelo: {importance['soil_type']:.2%}")
print(f"   - Tipo de cultivo: {importance['crop_type']:.2%}")
print(f"   - Historial de cosechas: {importance['harvest_count']:.2%}")

# 4. Hacer predicciones de prueba
print("\n4. Generando predicciones de prueba...")
forecaster = ProductionForecaster()

parcels = Parcel.objects.all()[:3]  # Primeras 3 parcelas
for parcel in parcels:
    prediction = forecaster.forecast_parcel_production(parcel.id)
    if prediction:
        print(f"\n   Parcela: {prediction['parcel_code']}")
        print(f"   - Rendimiento predicho: {prediction['predicted_yield']} kg/ha")
        print(f"   - Producción predicha: {prediction['predicted_production']} kg")
        print(f"   - Promedio histórico: {prediction['historical_avg']} kg")
        print(f"   - Recomendación: {prediction['recommendation']}")

# 5. Predicción por socio
print("\n5. Predicción por socio...")
partner = Partner.objects.first()
if partner:
    partner_pred = forecaster.forecast_partner_production(partner.id)
    if partner_pred:
        print(f"\n   Socio: {partner_pred['partner_name']}")
        print(f"   - Producción total predicha: {partner_pred['total_predicted_production']} kg")
        print(f"   - Número de parcelas: {partner_pred['parcels_count']}")

print("\n" + "=" * 60)
print("✓ PRUEBA COMPLETADA EXITOSAMENTE")
print("=" * 60)
print("\nEl sistema de ML está listo para usar!")
print("Puedes acceder a la interfaz web en: /reportes/ia")
