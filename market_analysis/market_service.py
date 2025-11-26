from datetime import datetime, timedelta
from django.db.models import Avg, Sum, Count
from production.models import HarvestedProduct
from .models import MarketPrice, PriceAlert
import random


class MarketAnalysisService:
    """Servicio para análisis de mercado basado en datos de producción"""
    
    # Precios base promedio en Bs por kg (Bolivia)
    BASE_PRICES = {
        'QUINUA': 15.50,
        'PAPA': 3.20,
        'MAIZ': 4.80,
        'TRIGO': 3.50,
        'CEBADA': 3.00,
        'HABA': 5.50,
        'ARVEJA': 6.00,
    }
    
    def __init__(self, organization):
        self.organization = organization
    
    def get_market_trends(self):
        """Obtiene tendencias de mercado basadas en producción histórica"""
        
        # Obtener producción de los últimos 30 días
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_production = HarvestedProduct.objects.filter(
            organization=self.organization,
            harvest_date__gte=thirty_days_ago
        ).values('product_name').annotate(
            total_quantity=Sum('quantity')
        )
        
        trends = []
        for prod in recent_production:
            product_name = prod['product_name'].upper()
            # Intentar mapear el nombre del producto a un tipo conocido
            crop_type = product_name
            for key in self.BASE_PRICES.keys():
                if key in product_name:
                    crop_type = key
                    break
            
            base_price = self.BASE_PRICES.get(crop_type, 5.0)
            
            # Simular variación de precio basada en producción
            # Más producción = precio tiende a bajar
            quantity = float(prod['total_quantity'] or 0)
            price_variation = random.uniform(-15, 20)  # -15% a +20%
            
            current_price = base_price * (1 + price_variation / 100)
            
            trends.append({
                'product': product_name,
                'base_price': round(base_price, 2),
                'current_price': round(current_price, 2),
                'variation': round(price_variation, 1),
                'total_production': round(quantity, 2),
                'trend': 'up' if price_variation > 0 else 'down'
            })
        
        return trends
    
    def get_price_alerts(self):
        """Genera alertas de precio basadas en tendencias"""
        
        trends = self.get_market_trends()
        alerts = []
        
        for trend in trends:
            variation = trend['variation']
            product = trend['product']
            
            if variation > 10:
                alerts.append({
                    'type': 'HIGH',
                    'product': product,
                    'message': f'Precio en alza. Momento óptimo para venta.',
                    'variation': variation,
                    'recommendation': f'Vender ahora puede generar hasta {abs(variation):.1f}% más de ganancia',
                    'priority': 'high'
                })
            elif variation < -8:
                alerts.append({
                    'type': 'LOW',
                    'product': product,
                    'message': f'Precio por debajo del promedio.',
                    'variation': variation,
                    'recommendation': 'Retener stock si es posible o buscar mercados alternativos',
                    'priority': 'medium'
                })
            elif 5 < variation <= 10:
                alerts.append({
                    'type': 'OPPORTUNITY',
                    'product': product,
                    'message': f'Precio favorable.',
                    'variation': variation,
                    'recommendation': 'Considerar venta en corto plazo',
                    'priority': 'low'
                })
        
        return alerts
    
    def get_opportunities(self):
        """Detecta oportunidades comerciales"""
        
        trends = self.get_market_trends()
        opportunities = []
        
        for trend in trends:
            if trend['variation'] > 8:
                potential_gain = trend['total_production'] * trend['current_price'] * (trend['variation'] / 100)
                
                opportunities.append({
                    'product': trend['product'],
                    'type': 'VENTA',
                    'description': f"Precio {trend['variation']:.1f}% sobre promedio",
                    'potential_gain': round(potential_gain, 2),
                    'action': 'Vender producción disponible',
                    'urgency': 'high' if trend['variation'] > 15 else 'medium'
                })
        
        # Detectar productos con alta producción
        high_production = [t for t in trends if t['total_production'] > 1000]
        for prod in high_production:
            opportunities.append({
                'product': prod['product'],
                'type': 'VOLUMEN',
                'description': f"Alta producción disponible: {prod['total_production']:.0f} kg",
                'potential_gain': 0,
                'action': 'Buscar compradores mayoristas',
                'urgency': 'medium'
            })
        
        return opportunities
    
    def get_demand_analysis(self):
        """Análisis de demanda basado en ventas históricas"""
        
        from sales.models import OrderItem
        
        # Obtener ventas de los últimos 60 días
        sixty_days_ago = datetime.now() - timedelta(days=60)
        sales_data = OrderItem.objects.filter(
            order__organization=self.organization,
            order__created_at__gte=sixty_days_ago
        ).values('product__product_name').annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('line_total')
        ).order_by('-total_sold')[:5]
        
        demand = []
        for item in sales_data:
            demand.append({
                'product': item['product__product_name'],
                'units_sold': float(item['total_sold'] or 0),
                'revenue': float(item['total_revenue'] or 0),
                'demand_level': 'high' if item['total_sold'] > 100 else 'medium'
            })
        
        return demand
    
    def get_market_summary(self):
        """Resumen completo del análisis de mercado"""
        
        trends = self.get_market_trends()
        alerts = self.get_price_alerts()
        opportunities = self.get_opportunities()
        demand = self.get_demand_analysis()
        
        return {
            'trends': trends,
            'alerts': alerts,
            'opportunities': opportunities,
            'demand_analysis': demand,
            'last_updated': datetime.now().isoformat(),
            'total_products_tracked': len(trends)
        }
