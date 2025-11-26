"""
Sistema de predicciones con Random Forest para reportes agrícolas
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from django.db.models import Avg, Sum, Count
from production.models import HarvestedProduct
from parcels.models import Parcel
from partners.models import Partner
import joblib
import os


class YieldPredictor:
    """Predictor de rendimiento usando Random Forest"""
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.is_trained = False
        self.model_path = 'reports/models/yield_predictor.pkl'
    
    def prepare_training_data(self):
        """Prepara datos de entrenamiento desde la base de datos"""
        parcels = Parcel.objects.all().select_related('partner', 'soil_type', 'current_crop')
        
        X = []  # Features
        y = []  # Target (rendimiento)
        
        for parcel in parcels:
            # Obtener producción histórica
            production = HarvestedProduct.objects.filter(parcel=parcel)
            
            # Crear una muestra por cada registro de producción
            for prod in production:
                if parcel.surface and float(parcel.surface) > 0 and prod.quantity:
                    # Features: superficie, tipo de suelo (encoded), cultivo (encoded)
                    features = [
                        float(parcel.surface),
                        hash(str(parcel.soil_type_id)) % 100,  # Simple encoding
                        hash(str(parcel.current_crop_id)) % 100,
                        production.count(),  # Número de cosechas
                    ]
                    
                    # Target: rendimiento (kg/ha) de esta cosecha específica
                    yield_value = float(prod.quantity) / float(parcel.surface)
                    
                    X.append(features)
                    y.append(yield_value)
        
        return np.array(X), np.array(y)
    
    def train(self):
        """Entrena el modelo con datos históricos"""
        X, y = self.prepare_training_data()
        
        if len(X) < 10:
            return {
                'success': False,
                'message': 'Datos insuficientes para entrenar (mínimo 10 registros)'
            }
        
        # Dividir en train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Entrenar
        self.model.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluar
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        # Guardar modelo
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump(self.model, self.model_path)
        
        return {
            'success': True,
            'train_score': train_score,
            'test_score': test_score,
            'samples': len(X),
            'message': f'Modelo entrenado con {len(X)} muestras'
        }
    
    def load_model(self):
        """Carga modelo previamente entrenado"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            return True
        return False
    
    def predict_yield(self, surface, soil_type_id, crop_id, harvest_count=1):
        """Predice el rendimiento para una parcela"""
        if not self.is_trained:
            if not self.load_model():
                return None
        
        features = np.array([[
            float(surface),
            hash(str(soil_type_id)) % 100,
            hash(str(crop_id)) % 100,
            harvest_count
        ]])
        
        prediction = self.model.predict(features)[0]
        return max(0, prediction)  # No permitir valores negativos
    
    def get_feature_importance(self):
        """Retorna la importancia de cada feature"""
        if not self.is_trained:
            return None
        
        return {
            'surface': self.model.feature_importances_[0],
            'soil_type': self.model.feature_importances_[1],
            'crop_type': self.model.feature_importances_[2],
            'harvest_count': self.model.feature_importances_[3]
        }


class ProductionForecaster:
    """Predictor de producción futura"""
    
    def __init__(self):
        self.yield_predictor = YieldPredictor()
    
    def forecast_parcel_production(self, parcel_id):
        """Predice la producción futura de una parcela"""
        try:
            parcel = Parcel.objects.get(id=parcel_id)
            
            # Obtener historial
            production = HarvestedProduct.objects.filter(parcel=parcel)
            harvest_count = production.count()
            
            # Predecir rendimiento
            predicted_yield = self.yield_predictor.predict_yield(
                surface=parcel.surface,
                soil_type_id=parcel.soil_type_id,
                crop_id=parcel.current_crop_id,
                harvest_count=harvest_count + 1
            )
            
            if predicted_yield is None:
                return None
            
            # Calcular producción total predicha
            predicted_production = predicted_yield * float(parcel.surface)
            
            # Obtener producción histórica promedio
            avg_production = production.aggregate(Avg('quantity'))['quantity__avg'] or 0
            
            return {
                'parcel_id': parcel.id,
                'parcel_code': parcel.code,
                'predicted_yield': round(predicted_yield, 2),
                'predicted_production': round(predicted_production, 2),
                'historical_avg': round(float(avg_production), 2),
                'confidence': 'medium',  # Podría calcularse con intervalos de confianza
                'recommendation': self._generate_recommendation(predicted_yield, avg_production)
            }
        except Parcel.DoesNotExist:
            return None
    
    def forecast_partner_production(self, partner_id):
        """Predice la producción total de un socio"""
        try:
            partner = Partner.objects.get(id=partner_id)
            parcels = partner.parcels.all()
            
            total_predicted = 0
            parcel_predictions = []
            
            for parcel in parcels:
                prediction = self.forecast_parcel_production(parcel.id)
                if prediction:
                    total_predicted += prediction['predicted_production']
                    parcel_predictions.append(prediction)
            
            return {
                'partner_id': partner.id,
                'partner_name': partner.full_name,
                'total_predicted_production': round(total_predicted, 2),
                'parcels_count': len(parcel_predictions),
                'parcel_predictions': parcel_predictions
            }
        except Partner.DoesNotExist:
            return None
    
    def _generate_recommendation(self, predicted_yield, historical_avg):
        """Genera recomendación basada en predicción"""
        historical_avg = float(historical_avg) if historical_avg else 0
        
        if historical_avg == 0:
            return "Datos históricos insuficientes"
        
        change = ((predicted_yield - historical_avg) / historical_avg) * 100
        
        if change > 10:
            return f"Excelente: Se espera un aumento del {change:.1f}% en el rendimiento"
        elif change > 0:
            return f"Bueno: Se espera un aumento del {change:.1f}% en el rendimiento"
        elif change > -10:
            return f"Atención: Se espera una disminución del {abs(change):.1f}% en el rendimiento"
        else:
            return f"Alerta: Se espera una disminución significativa del {abs(change):.1f}%"
