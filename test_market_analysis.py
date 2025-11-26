"""
Script para probar el análisis de mercado
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from market_analysis.market_service import MarketAnalysisService
from tenants.models import Organization
from users.models import User

def test_market_analysis():
    """Prueba el servicio de análisis de mercado"""
    
    # Obtener la primera organización
    org = Organization.objects.first()
    if not org:
        print("❌ No hay organizaciones en el sistema")
        return
    
    print(f"✅ Probando análisis de mercado para: {org.name}")
    print("-" * 60)
    
    # Crear servicio
    service = MarketAnalysisService(org)
    
    # Obtener resumen completo
    try:
        summary = service.get_market_summary()
        
        print(f"\n📊 RESUMEN DEL ANÁLISIS DE MERCADO")
        print(f"Última actualización: {summary['last_updated']}")
        print(f"Productos rastreados: {summary['total_products_tracked']}")
        
        # Tendencias
        print(f"\n📈 TENDENCIAS DE PRECIO ({len(summary['trends'])} productos)")
        for trend in summary['trends']:
            symbol = "📈" if trend['variation'] > 0 else "📉"
            print(f"  {symbol} {trend['product']}: Bs. {trend['current_price']}/kg ({trend['variation']:+.1f}%)")
            print(f"     Producción: {trend['total_production']:.2f} kg")
        
        # Alertas
        print(f"\n⚠️  ALERTAS ACTIVAS ({len(summary['alerts'])} alertas)")
        for alert in summary['alerts']:
            print(f"  • {alert['product']}: {alert['message']}")
            print(f"    Recomendación: {alert['recommendation']}")
        
        # Oportunidades
        print(f"\n💰 OPORTUNIDADES COMERCIALES ({len(summary['opportunities'])} oportunidades)")
        for opp in summary['opportunities']:
            urgency_icon = "🔴" if opp['urgency'] == 'high' else "🟡"
            print(f"  {urgency_icon} {opp['product']} - {opp['type']}")
            print(f"     {opp['description']}")
            if opp['potential_gain'] > 0:
                print(f"     Ganancia potencial: Bs. {opp['potential_gain']:.2f}")
        
        # Análisis de demanda
        print(f"\n📊 ANÁLISIS DE DEMANDA ({len(summary['demand_analysis'])} productos)")
        for demand in summary['demand_analysis']:
            print(f"  • {demand['product']}: {demand['units_sold']:.0f} unidades vendidas")
            print(f"    Ingresos: Bs. {demand['revenue']:.2f}")
        
        print("\n" + "=" * 60)
        print("✅ Análisis completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error al generar análisis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_market_analysis()
