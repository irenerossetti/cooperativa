"""
Script para convertir automáticamente los modelos a TenantModel.

Este script modifica los archivos models.py para:
1. Importar TenantModel
2. Cambiar herencia de models.Model a TenantModel
3. Actualizar campos unique a unique_together
4. Agregar comentarios explicativos

IMPORTANTE: Haz backup antes de ejecutar este script!

Uso:
    python convert_models_to_tenant.py --dry-run  # Ver cambios sin aplicar
    python convert_models_to_tenant.py --apply    # Aplicar cambios
"""

import os
import re
import argparse
from pathlib import Path


# Apps que contienen modelos de negocio
BUSINESS_APPS = [
    'partners', 'parcels', 'campaigns', 'farm_activities',
    'inventory', 'production', 'sales', 'requests',
    'pricing', 'shipping', 'financial', 'reports',
    'traceability', 'analytics', 'ai_recommendations',
    'monitoring', 'weather', 'audit'
]


def backup_file(file_path):
    """Crea un backup del archivo."""
    backup_path = f"{file_path}.backup"
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return backup_path


def add_tenant_import(content):
    """Agrega el import de TenantModel si no existe."""
    if 'from tenants.managers import TenantModel' in content:
        return content, False
    
    # Buscar la última línea de imports
    lines = content.split('\n')
    last_import_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('from ') or line.startswith('import '):
            last_import_idx = i
    
    # Insertar el import después del último import
    lines.insert(last_import_idx + 1, 'from tenants.managers import TenantModel')
    
    return '\n'.join(lines), True


def convert_model_inheritance(content):
    """Convierte models.Model a TenantModel."""
    # Patrón para encontrar clases que heredan de models.Model
    pattern = r'class\s+(\w+)\(models\.Model\):'
    
    def replace_func(match):
        class_name = match.group(1)
        return f'class {class_name}(TenantModel):'
    
    new_content = re.sub(pattern, replace_func, content)
    changed = new_content != content
    
    return new_content, changed


def find_unique_fields(content):
    """Encuentra campos con unique=True."""
    pattern = r'(\w+)\s*=\s*models\.\w+Field\([^)]*unique=True[^)]*\)'
    matches = re.findall(pattern, content)
    return matches


def suggest_unique_together(model_content, unique_fields):
    """Sugiere cambios para unique_together."""
    suggestions = []
    
    for field in unique_fields:
        suggestions.append(f"  # TODO: Cambiar {field} de unique=True a unique_together")
        suggestions.append(f"  # En Meta: unique_together = [['organization', '{field}']]")
    
    return suggestions


def process_models_file(file_path, dry_run=True):
    """Procesa un archivo models.py."""
    print(f"\n{'='*70}")
    print(f"📄 Procesando: {file_path}")
    print(f"{'='*70}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    content = original_content
    changes_made = []
    
    # 1. Agregar import de TenantModel
    content, changed = add_tenant_import(content)
    if changed:
        changes_made.append("✅ Agregado import de TenantModel")
    
    # 2. Convertir herencia
    content, changed = convert_model_inheritance(content)
    if changed:
        changes_made.append("✅ Convertida herencia a TenantModel")
    
    # 3. Encontrar campos unique
    unique_fields = find_unique_fields(content)
    if unique_fields:
        changes_made.append(f"⚠️  Campos unique encontrados: {', '.join(unique_fields)}")
        suggestions = suggest_unique_together(content, unique_fields)
        for suggestion in suggestions:
            changes_made.append(suggestion)
    
    # Mostrar cambios
    if changes_made:
        for change in changes_made:
            print(change)
        
        if not dry_run:
            # Crear backup
            backup_path = backup_file(file_path)
            print(f"💾 Backup creado: {backup_path}")
            
            # Guardar cambios
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Archivo actualizado")
        else:
            print(f"🔍 Modo dry-run: No se aplicaron cambios")
    else:
        print("ℹ️  No se requieren cambios")
    
    return len(changes_made) > 0


def main():
    parser = argparse.ArgumentParser(description='Convertir modelos a TenantModel')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--apply', action='store_true', help='Aplicar cambios')
    group.add_argument('--dry-run', action='store_true', help='Solo mostrar cambios sin aplicar (por defecto)')
    parser.add_argument('--app', type=str, help='Procesar solo una app específica')
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    print("=" * 70)
    print("🔧 CONVERSIÓN DE MODELOS A MULTI-TENANT")
    print("=" * 70)
    
    if dry_run:
        print("🔍 Modo: DRY-RUN (solo mostrar cambios)")
    else:
        print("⚠️  Modo: APLICAR CAMBIOS")
        response = input("¿Estás seguro? Se crearán backups. (s/n): ")
        if response.lower() != 's':
            print("❌ Operación cancelada")
            return
    
    print()
    
    # Determinar qué apps procesar
    apps_to_process = [args.app] if args.app else BUSINESS_APPS
    
    files_processed = 0
    files_changed = 0
    
    for app_name in apps_to_process:
        # Intentar con y sin prefijo Backend/
        models_file = Path(f'{app_name}/models.py')
        if not models_file.exists():
            models_file = Path(f'Backend/{app_name}/models.py')
        
        if not models_file.exists():
            print(f"⚠️  {app_name}/models.py no encontrado")
            continue
        
        files_processed += 1
        if process_models_file(models_file, dry_run):
            files_changed += 1
    
    print()
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    print(f"Archivos procesados: {files_processed}")
    print(f"Archivos con cambios: {files_changed}")
    
    if dry_run:
        print()
        print("💡 Para aplicar los cambios, ejecuta:")
        print("   python convert_models_to_tenant.py --apply")
    else:
        print()
        print("✅ Cambios aplicados!")
        print()
        print("📝 Próximos pasos:")
        print("1. Revisa los archivos modificados")
        print("2. Actualiza campos unique a unique_together manualmente")
        print("3. Ejecuta: python manage.py makemigrations")
        print("4. Ejecuta: python manage.py migrate")
        print("5. Ejecuta: python migrate_to_multitenant.py")


if __name__ == '__main__':
    main()
