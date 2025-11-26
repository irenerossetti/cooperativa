"""
Script para probar el tracking automático de auditoría
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from audit.models import AuditLog
from django.utils import timezone
from datetime import timedelta

def check_recent_audit_logs():
    """Verificar los logs de auditoría recientes"""
    print("\n" + "="*70)
    print("LOGS DE AUDITORÍA RECIENTES (Últimas 24 horas)")
    print("="*70)
    
    # Obtener logs de las últimas 24 horas
    yesterday = timezone.now() - timedelta(days=1)
    recent_logs = AuditLog.objects.filter(
        timestamp__gte=yesterday
    ).select_related('user').order_by('-timestamp')[:50]
    
    if not recent_logs.exists():
        print("\n❌ No hay logs de auditoría recientes")
        print("   Realiza algunas acciones en el sistema (crear, editar, eliminar)")
        return
    
    print(f"\n✅ Se encontraron {recent_logs.count()} logs recientes\n")
    
    # Agrupar por acción
    actions_count = {}
    models_count = {}
    
    for log in recent_logs:
        action = log.get_action_display()
        actions_count[action] = actions_count.get(action, 0) + 1
        
        model = log.model_name or 'Unknown'
        models_count[model] = models_count.get(model, 0) + 1
    
    # Mostrar resumen
    print("📊 RESUMEN POR ACCIÓN:")
    print("-" * 70)
    for action, count in sorted(actions_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {action:20} : {count:3} registros")
    
    print("\n📊 RESUMEN POR MODELO:")
    print("-" * 70)
    for model, count in sorted(models_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {model:20} : {count:3} registros")
    
    # Mostrar últimos 10 logs
    print("\n📝 ÚLTIMOS 10 REGISTROS:")
    print("-" * 70)
    print(f"{'FECHA/HORA':<20} {'USUARIO':<15} {'ACCIÓN':<15} {'MODELO':<15} {'DESCRIPCIÓN':<30}")
    print("-" * 70)
    
    for log in recent_logs[:10]:
        timestamp = log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        username = log.user.username if log.user else 'Sistema'
        action = log.get_action_display()
        model = log.model_name or '-'
        description = (log.description[:27] + '...') if len(log.description) > 30 else log.description
        
        print(f"{timestamp:<20} {username:<15} {action:<15} {model:<15} {description:<30}")
    
    print("\n" + "="*70)
    print("✅ Sistema de auditoría funcionando correctamente")
    print("="*70)


def check_audit_coverage():
    """Verificar qué modelos tienen auditoría"""
    print("\n" + "="*70)
    print("COBERTURA DE AUDITORÍA POR MODELO")
    print("="*70)
    
    # Obtener todos los modelos únicos en los logs
    models = AuditLog.objects.values_list('model_name', flat=True).distinct()
    
    if not models:
        print("\n❌ No hay logs de auditoría en el sistema")
        return
    
    print(f"\n✅ Modelos con auditoría: {len(models)}\n")
    
    for model in sorted(models):
        if model:
            count = AuditLog.objects.filter(model_name=model).count()
            print(f"  • {model:<20} : {count:5} registros")
    
    print("\n" + "="*70)


if __name__ == '__main__':
    print("\n🔍 VERIFICACIÓN DEL SISTEMA DE AUDITORÍA")
    check_recent_audit_logs()
    check_audit_coverage()
    
    print("\n💡 TIPS:")
    print("  • Realiza acciones en el sistema para generar más logs")
    print("  • Los logs se crean automáticamente al crear/editar/eliminar registros")
    print("  • Revisa la página de Auditoría en el frontend para ver los logs")
    print()
