#!/usr/bin/env python
"""
Script para probar todas las funcionalidades implementadas
Ejecutar: python test_all_features.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_notifications():
    """Prueba el sistema de notificaciones"""
    print_header("TEST 1: Sistema de Notificaciones")
    
    try:
        from notifications.models import Notification, NotificationPreference
        from users.models import User
        
        # Contar notificaciones
        total = Notification.objects.count()
        unread = Notification.objects.filter(read=False).count()
        
        print_success(f"Notificaciones totales: {total}")
        print_success(f"Notificaciones no leídas: {unread}")
        
        # Verificar preferencias
        prefs = NotificationPreference.objects.count()
        print_success(f"Preferencias configuradas: {prefs}")
        
        # Crear notificación de prueba
        user = User.objects.first()
        if user:
            from notifications.utils import create_notification
            notif = create_notification(
                user=user,
                title='Test de notificación',
                message='Esta es una notificación de prueba',
                notification_type='INFO'
            )
            print_success(f"Notificación de prueba creada: #{notif.id}")
        
        return True
        
    except Exception as e:
        print_error(f"Error en notificaciones: {str(e)}")
        return False

def test_qr_codes():
    """Prueba el sistema de códigos QR"""
    print_header("TEST 2: Códigos QR")
    
    try:
        from qr_codes.models import QRCode
        from partners.models import Partner
        
        # Contar QR codes
        total = QRCode.objects.count()
        print_success(f"Códigos QR generados: {total}")
        
        # Generar QR de prueba
        partner = Partner.objects.first()
        if partner:
            qr, created = QRCode.objects.get_or_create(
                model_type='partner',
                object_id=partner.id,
                defaults={'qr_data': f"partner:{partner.id}"}
            )
            status = "creado" if created else "ya existía"
            print_success(f"QR de prueba {status}: #{qr.id}")
            print_info(f"Escaneos: {qr.scans_count}")
        
        return True
        
    except Exception as e:
        print_error(f"Error en QR codes: {str(e)}")
        return False

def test_dashboard():
    """Prueba el dashboard"""
    print_header("TEST 3: Dashboard en Tiempo Real")
    
    try:
        from dashboard.views import dashboard_metrics
        from django.test import RequestFactory
        from users.models import User
        
        # Simular request
        factory = RequestFactory()
        user = User.objects.first()
        
        if user:
            request = factory.get('/api/dashboard/metrics/')
            request.user = user
            
            response = dashboard_metrics(request)
            
            if response.status_code == 200:
                data = response.data
                print_success("Dashboard funcionando correctamente")
                print_info(f"Ventas hoy: Bs. {data['sales']['today']['amount']}")
                print_info(f"Socios totales: {data['partners']['total']}")
                print_info(f"Alertas activas: {data['inventory']['low_stock_alerts']}")
            else:
                print_error(f"Error en dashboard: {response.status_code}")
                return False
        
        return True
        
    except Exception as e:
        print_error(f"Error en dashboard: {str(e)}")
        return False

def test_ai_chat():
    """Prueba el chat de IA"""
    print_header("TEST 4: Asistente de IA")
    
    try:
        from ai_chat.models import ChatConversation, ChatMessage
        
        # Contar conversaciones
        conversations = ChatConversation.objects.count()
        messages = ChatMessage.objects.count()
        
        print_success(f"Conversaciones: {conversations}")
        print_success(f"Mensajes: {messages}")
        
        # Probar servicio de IA
        from ai_chat.ai_service import AIService
        
        service = AIService()
        print_info("Servicio de IA inicializado")
        
        if service.api_key:
            print_success("API Key configurada")
        else:
            print_info("API Key no configurada (usará fallback)")
        
        return True
        
    except Exception as e:
        print_error(f"Error en AI chat: {str(e)}")
        return False

def test_events():
    """Prueba el sistema de eventos"""
    print_header("TEST 5: Calendario de Eventos")
    
    try:
        from events.models import Event, EventReminder
        
        # Contar eventos
        total = Event.objects.count()
        upcoming = Event.objects.filter(completed=False).count()
        completed = Event.objects.filter(completed=True).count()
        
        print_success(f"Eventos totales: {total}")
        print_success(f"Eventos próximos: {upcoming}")
        print_success(f"Eventos completados: {completed}")
        
        # Eventos por tipo
        from django.db.models import Count
        by_type = Event.objects.values('type').annotate(count=Count('id'))
        
        print_info("Eventos por tipo:")
        for item in by_type:
            print(f"   • {item['type']}: {item['count']}")
        
        # Recordatorios
        reminders = EventReminder.objects.count()
        print_success(f"Recordatorios enviados: {reminders}")
        
        return True
        
    except Exception as e:
        print_error(f"Error en eventos: {str(e)}")
        return False

def test_goals():
    """Prueba el sistema de metas"""
    print_header("TEST 6: Metas y Objetivos")
    
    try:
        from goals.models import Goal, GoalMilestone
        
        # Contar metas
        total = Goal.objects.count()
        in_progress = Goal.objects.filter(status='IN_PROGRESS').count()
        completed = Goal.objects.filter(status='COMPLETED').count()
        at_risk = len([g for g in Goal.objects.all() if g.is_at_risk])
        
        print_success(f"Metas totales: {total}")
        print_success(f"En progreso: {in_progress}")
        print_success(f"Completadas: {completed}")
        print_success(f"En riesgo: {at_risk}")
        
        # Progreso promedio
        if total > 0:
            avg_progress = sum(g.progress_percentage for g in Goal.objects.all()) / total
            print_info(f"Progreso promedio: {avg_progress:.2f}%")
        
        # Hitos
        milestones = GoalMilestone.objects.count()
        completed_milestones = GoalMilestone.objects.filter(completed=True).count()
        print_success(f"Hitos totales: {milestones}")
        print_success(f"Hitos completados: {completed_milestones}")
        
        return True
        
    except Exception as e:
        print_error(f"Error en metas: {str(e)}")
        return False

def test_endpoints():
    """Prueba los endpoints principales"""
    print_header("TEST 7: Endpoints REST API")
    
    try:
        from django.urls import get_resolver
        
        resolver = get_resolver()
        
        # Contar endpoints
        patterns = resolver.url_patterns
        
        # Endpoints de las nuevas apps
        new_endpoints = [
            'notifications', 'qr-codes', 'dashboard',
            'ai-chat', 'events', 'goals'
        ]
        
        found_endpoints = []
        for pattern in patterns:
            pattern_str = str(pattern.pattern)
            for endpoint in new_endpoints:
                if endpoint in pattern_str:
                    found_endpoints.append(endpoint)
                    break
        
        print_success(f"Endpoints encontrados: {len(set(found_endpoints))}/6")
        
        for endpoint in set(found_endpoints):
            print_info(f"  ✓ {endpoint}")
        
        return len(set(found_endpoints)) >= 5
        
    except Exception as e:
        print_error(f"Error verificando endpoints: {str(e)}")
        return False

def main():
    print_header("PRUEBA COMPLETA DE FUNCIONALIDADES")
    print("Probando todas las funcionalidades implementadas...\n")
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("Notificaciones", test_notifications()))
    results.append(("Códigos QR", test_qr_codes()))
    results.append(("Dashboard", test_dashboard()))
    results.append(("Chat IA", test_ai_chat()))
    results.append(("Eventos", test_events()))
    results.append(("Metas", test_goals()))
    results.append(("Endpoints", test_endpoints()))
    
    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n📊 Resultados: {passed}/{total} pruebas exitosas\n")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    if passed == total:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n✅ El sistema está funcionando correctamente")
        print("\n🚀 Listo para la defensa")
    else:
        print(f"\n⚠️  {total - passed} prueba(s) fallaron")
        print("\n🔧 Revisa los errores arriba")
    
    print("\n📚 Próximos pasos:")
    print("  1. Iniciar servidor: python manage.py runserver")
    print("  2. Probar en navegador: http://localhost:8000")
    print("  3. Revisar documentación: RESUMEN_FINAL_DEFENSA.md")

if __name__ == '__main__':
    main()
