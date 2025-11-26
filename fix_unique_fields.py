"""
Script para ajustar automáticamente los campos unique=True a unique_together.

Este script:
1. Encuentra campos con unique=True
2. Los cambia a campos normales
3. Agrega unique_together en Meta

Uso:
    python fix_unique_fields.py
"""

import re
from pathlib import Path


# Mapeo de archivos y campos unique que deben ajustarse
UNIQUE_FIELDS_MAP = {
    'partners/models.py': {
        'Community': ['name'],
        'Partner': ['ci', 'nit']
    },
    'parcels/models.py': {
        'SoilType': ['name'],
        'Crop': ['name'],
        'Parcel': ['code']
    },
    'campaigns/models.py': {
        'Campaign': ['code']
    },
    'farm_activities/models.py': {
        'ActivityType': ['name']
    },
    'inventory/models.py': {
        'InventoryCategory': ['name'],
        'InventoryItem': ['code']
    },
    'sales/models.py': {
        'PaymentMethod': ['name'],
        'Customer': ['document_number'],
        'Order': ['order_number']
    },
    'requests/models.py': {
        'RequestType': ['name'],
        'PartnerRequest': ['request_number']
    },
    'pricing/models.py': {
        'PriceList': ['code']
    },
    'shipping/models.py': {
        'Shipment': ['shipment_number']
    },
    'financial/models.py': {
        'ExpenseCategory': ['name']
    },
    'reports/models.py': {
        'ReportType': ['name']
    },
    'traceability/models.py': {
        'ParcelTraceability': ['traceability_code']
    },
    'ai_recommendations/models.py': {
        'AIRecommendationType': ['name']
    }
}


def remove_unique_from_field(content, field_name):
    """Remueve unique=True de un campo."""
    # Patrón para encontrar el campo con unique=True
    patterns = [
        # Caso 1: unique=True al final
        (rf'({field_name}\s*=\s*models\.\w+Field\([^)]*)(,\s*unique=True)(\s*\))', r'\1\3'),
        # Caso 2: unique=True en medio
        (rf'({field_name}\s*=\s*models\.\w+Field\([^)]*)(unique=True,\s*)([^)]*\))', r'\1\3'),
        # Caso 3: unique=True solo
        (rf'({field_name}\s*=\s*models\.\w+Field\()(unique=True)(\))', r'\1\3'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    return content


def add_unique_together_to_meta(content, model_name, fields):
    """Agrega unique_together a la clase Meta del modelo."""
    
    # Buscar la clase del modelo
    model_pattern = rf'class {model_name}\(TenantModel\):(.*?)(?=class\s+\w+|$)'
    model_match = re.search(model_pattern, content, re.DOTALL)
    
    if not model_match:
        return content, False
    
    model_content = model_match.group(0)
    
    # Buscar si ya existe clase Meta
    meta_pattern = r'class Meta:(.*?)(?=\n    [a-z_]|\n\n|\Z)'
    meta_match = re.search(meta_pattern, model_content, re.DOTALL)
    
    if meta_match:
        # Ya existe Meta, agregar unique_together
        meta_content = meta_match.group(0)
        
        # Verificar si ya existe unique_together
        if 'unique_together' in meta_content:
            return content, False
        
        # Agregar unique_together al final de Meta
        unique_together_lines = []
        for field in fields:
            unique_together_lines.append(f"            ['organization', '{field}'],")
        
        unique_together_str = '\n'.join(unique_together_lines)
        
        # Encontrar la última línea de Meta
        lines = meta_content.split('\n')
        # Insertar antes del último elemento (que suele ser una línea vacía o el cierre)
        insert_pos = len(lines) - 1
        
        new_meta = '\n'.join(lines[:insert_pos]) + f'\n        unique_together = [\n{unique_together_str}\n        ]\n' + '\n'.join(lines[insert_pos:])
        
        content = content.replace(meta_content, new_meta)
        return content, True
    else:
        # No existe Meta, crearla
        unique_together_lines = []
        for field in fields:
            unique_together_lines.append(f"            ['organization', '{field}'],")
        
        unique_together_str = '\n'.join(unique_together_lines)
        
        # Buscar el final de la clase (antes del siguiente def o class)
        class_end_pattern = rf'(class {model_name}\(TenantModel\):.*?)(\n    def |\n\nclass |\Z)'
        
        meta_class = f'''
    class Meta:
        unique_together = [
{unique_together_str}
        ]
'''
        
        content = re.sub(
            class_end_pattern,
            rf'\1{meta_class}\2',
            content,
            flags=re.DOTALL
        )
        
        return content, True


def process_file(file_path, models_fields):
    """Procesa un archivo de modelos."""
    print(f"\n{'='*70}")
    print(f"📄 Procesando: {file_path}")
    print(f"{'='*70}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = []
    
    for model_name, fields in models_fields.items():
        print(f"\n🔧 Modelo: {model_name}")
        
        # Remover unique=True de los campos
        for field in fields:
            content = remove_unique_from_field(content, field)
            print(f"   ✅ Removido unique=True de '{field}'")
        
        # Agregar unique_together
        content, added = add_unique_together_to_meta(content, model_name, fields)
        if added:
            print(f"   ✅ Agregado unique_together para {fields}")
            changes_made.append(model_name)
        else:
            print(f"   ℹ️  unique_together ya existe o no se pudo agregar")
    
    if content != original_content:
        # Crear backup
        backup_path = f"{file_path}.backup2"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(original_content)
        print(f"\n💾 Backup creado: {backup_path}")
        
        # Guardar cambios
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Archivo actualizado")
        return True
    else:
        print(f"\nℹ️  No se requieren cambios")
        return False


def main():
    print("="*70)
    print("🔧 AJUSTE DE CAMPOS UNIQUE")
    print("="*70)
    print("\nEste script ajustará los campos unique=True a unique_together")
    print()
    
    response = input("¿Continuar? (s/n): ")
    if response.lower() != 's':
        print("❌ Operación cancelada")
        return
    
    files_processed = 0
    files_changed = 0
    
    for file_path, models_fields in UNIQUE_FIELDS_MAP.items():
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"⚠️  {file_path} no encontrado")
            continue
        
        files_processed += 1
        if process_file(file_path, models_fields):
            files_changed += 1
    
    print()
    print("="*70)
    print("📊 RESUMEN")
    print("="*70)
    print(f"Archivos procesados: {files_processed}")
    print(f"Archivos modificados: {files_changed}")
    print()
    print("📝 Próximos pasos:")
    print("1. Revisa los archivos modificados")
    print("2. Ejecuta: python manage.py makemigrations")
    print("3. Ejecuta: python manage.py migrate")
    print("4. Ejecuta: python migrate_to_multitenant.py")


if __name__ == '__main__':
    main()
