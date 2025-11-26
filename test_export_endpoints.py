"""
Script para probar los endpoints de exportación
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from reports.views import ReportViewSet

def test_export_methods():
    """Probar que los métodos de exportación existen"""
    viewset = ReportViewSet()
    
    print("🧪 Probando métodos de exportación...\n")
    
    # Verificar que los métodos existen
    methods = [
        '_get_performance_data',
        '_get_population_data',
        '_get_hectares_data',
        '_get_parcel_performance_data',
        '_get_partners_by_community_data',
        '_get_hectares_by_crop_data'
    ]
    
    for method_name in methods:
        if hasattr(viewset, method_name):
            print(f"✅ {method_name} existe")
        else:
            print(f"❌ {method_name} NO existe")

if __name__ == '__main__':
    test_export_methods()
