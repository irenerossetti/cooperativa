from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from decimal import Decimal


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_metrics(request):
    """
    Obtiene métricas en tiempo real para el dashboard
    """
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    this_month_start = today.replace(day=1)
    last_month_start = (this_month_start - timedelta(days=1)).replace(day=1)
    
    # Importar modelos
    from partners.models import Partner
    from parcels.models import Parcel
    from sales.models import Order
    from inventory.models import InventoryItem, StockAlert
    from production.models import HarvestedProduct
    from requests.models import PartnerRequest
    from campaigns.models import Campaign
    
    # 1. VENTAS
    sales_today = Order.objects.filter(
        order_date__date=today
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    
    sales_yesterday = Order.objects.filter(
        order_date__date=yesterday
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    
    sales_this_month = Order.objects.filter(
        order_date__gte=this_month_start
    ).aggregate(
        total=Sum('total_amount'),
        count=Count('id')
    )
    
    # Calcular cambio porcentual
    sales_change = calculate_percentage_change(
        sales_today['total'] or 0,
        sales_yesterday['total'] or 0
    )
    
    # 2. SOCIOS
    total_partners = Partner.objects.filter(status='ACTIVE').count()
    new_partners_today = Partner.objects.filter(
        registration_date=today
    ).count()
    
    # 3. PRODUCCIÓN
    production_today = HarvestedProduct.objects.filter(
        harvest_date__date=today
    ).aggregate(
        total=Sum('quantity'),
        count=Count('id')
    )
    
    production_this_month = HarvestedProduct.objects.filter(
        harvest_date__gte=this_month_start
    ).aggregate(
        total=Sum('quantity')
    )
    
    # 4. INVENTARIO
    low_stock_items = StockAlert.objects.filter(
        resolved=False
    ).count()
    
    total_inventory_value = InventoryItem.objects.aggregate(
        total=Sum('current_stock')
    )['total'] or 0
    
    # 5. SOLICITUDES
    pending_requests = PartnerRequest.objects.filter(
        status='PENDING'
    ).count()
    
    requests_today = PartnerRequest.objects.filter(
        created_at__date=today
    ).count()
    
    # 6. CAMPAÑAS
    active_campaigns = Campaign.objects.filter(
        status='ACTIVE'
    ).count()
    
    # 7. PARCELAS
    total_parcels = Parcel.objects.filter(status='ACTIVE').count()
    total_surface = Parcel.objects.filter(
        status='ACTIVE'
    ).aggregate(
        total=Sum('surface')
    )['total'] or 0
    
    # 8. ACTIVIDAD RECIENTE (últimas 24 horas)
    recent_activity = {
        'new_orders': Order.objects.filter(
            order_date__gte=timezone.now() - timedelta(hours=24)
        ).count(),
        'new_requests': PartnerRequest.objects.filter(
            created_at__gte=timezone.now() - timedelta(hours=24)
        ).count(),
        'new_production': HarvestedProduct.objects.filter(
            harvest_date__gte=timezone.now() - timedelta(hours=24)
        ).count(),
    }
    
    # 9. TENDENCIAS (últimos 7 días)
    sales_trend = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_sales = Order.objects.filter(
            order_date__date=date
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        sales_trend.append({
            'date': date.isoformat(),
            'value': float(daily_sales)
        })
    
    # 10. TOP PRODUCTOS MÁS VENDIDOS (este mes)
    from sales.models import OrderItem
    top_products = OrderItem.objects.filter(
        order__order_date__gte=this_month_start
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum('subtotal')
    ).order_by('-total_quantity')[:5]
    
    # Construir respuesta
    metrics = {
        'timestamp': timezone.now().isoformat(),
        
        # Ventas
        'sales': {
            'today': {
                'amount': float(sales_today['total'] or 0),
                'count': sales_today['count'] or 0,
                'change': sales_change
            },
            'this_month': {
                'amount': float(sales_this_month['total'] or 0),
                'count': sales_this_month['count'] or 0
            },
            'trend': sales_trend
        },
        
        # Socios
        'partners': {
            'total': total_partners,
            'new_today': new_partners_today,
            'active': total_partners
        },
        
        # Producción
        'production': {
            'today': {
                'quantity': float(production_today['total'] or 0),
                'count': production_today['count'] or 0
            },
            'this_month': {
                'quantity': float(production_this_month['total'] or 0)
            }
        },
        
        # Inventario
        'inventory': {
            'low_stock_alerts': low_stock_items,
            'total_items': total_inventory_value
        },
        
        # Solicitudes
        'requests': {
            'pending': pending_requests,
            'today': requests_today
        },
        
        # Campañas
        'campaigns': {
            'active': active_campaigns
        },
        
        # Parcelas
        'parcels': {
            'total': total_parcels,
            'total_surface': float(total_surface)
        },
        
        # Actividad reciente
        'recent_activity': recent_activity,
        
        # Top productos
        'top_products': [
            {
                'name': item['product__name'],
                'quantity': float(item['total_quantity']),
                'amount': float(item['total_amount'])
            }
            for item in top_products
        ]
    }
    
    return Response(metrics)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Resumen rápido para polling frecuente
    """
    from sales.models import Order
    from requests.models import PartnerRequest
    from inventory.models import StockAlert
    from notifications.models import Notification
    
    today = timezone.now().date()
    
    summary = {
        'timestamp': timezone.now().isoformat(),
        'sales_today_count': Order.objects.filter(order_date__date=today).count(),
        'pending_requests': PartnerRequest.objects.filter(status='PENDING').count(),
        'low_stock_alerts': StockAlert.objects.filter(resolved=False).count(),
        'unread_notifications': Notification.objects.filter(
            user=request.user,
            read=False
        ).count(),
    }
    
    return Response(summary)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_charts(request):
    """
    Datos para gráficos del dashboard
    """
    from sales.models import Order
    from production.models import HarvestedProduct
    from partners.models import Partner
    
    today = timezone.now().date()
    
    # Gráfico de ventas (últimos 30 días)
    sales_chart = []
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        daily_sales = Order.objects.filter(
            order_date__date=date
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        
        sales_chart.append({
            'date': date.isoformat(),
            'amount': float(daily_sales['total'] or 0),
            'orders': daily_sales['count'] or 0
        })
    
    # Gráfico de producción (últimos 30 días)
    production_chart = []
    for i in range(29, -1, -1):
        date = today - timedelta(days=i)
        daily_production = HarvestedProduct.objects.filter(
            harvest_date__date=date
        ).aggregate(
            total=Sum('quantity')
        )
        
        production_chart.append({
            'date': date.isoformat(),
            'quantity': float(daily_production['total'] or 0)
        })
    
    # Distribución de socios por comunidad
    from partners.models import Community
    partners_by_community = []
    communities = Community.objects.all()
    
    for community in communities:
        count = Partner.objects.filter(
            community=community,
            status='ACTIVE'
        ).count()
        
        if count > 0:
            partners_by_community.append({
                'name': community.name,
                'value': count
            })
    
    # Distribución de cultivos
    from parcels.models import Parcel
    parcels_by_crop = Parcel.objects.filter(
        status='ACTIVE',
        current_crop__isnull=False
    ).values(
        'current_crop__name'
    ).annotate(
        count=Count('id'),
        surface=Sum('surface')
    ).order_by('-count')
    
    crops_distribution = [
        {
            'name': item['current_crop__name'],
            'parcels': item['count'],
            'surface': float(item['surface'])
        }
        for item in parcels_by_crop
    ]
    
    return Response({
        'sales_chart': sales_chart,
        'production_chart': production_chart,
        'partners_by_community': partners_by_community,
        'crops_distribution': crops_distribution
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def realtime_dashboard(request):
    """
    Dashboard en tiempo real - datos simplificados para actualización frecuente
    """
    from sales.models import Order, OrderItem
    from partners.models import Partner
    from inventory.models import InventoryItem
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Total de ventas (este mes)
    this_month_start = today.replace(day=1)
    total_sales = Order.objects.filter(
        order_date__gte=this_month_start
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Total de socios activos
    total_partners = Partner.objects.filter(status='ACTIVE').count()
    
    # Total de productos en inventario
    total_products = InventoryItem.objects.count()
    
    # Pedidos pendientes
    pending_orders = Order.objects.filter(status='PENDING').count()
    
    # Ventas últimos 7 días
    sales_chart = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_sales = Order.objects.filter(
            order_date__date=date
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        sales_chart.append({
            'date': date.strftime('%d/%m'),
            'amount': float(daily_sales)
        })
    
    # Top 5 productos más vendidos (últimos 7 días)
    top_products = OrderItem.objects.filter(
        order__order_date__gte=week_ago
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]
    
    top_products_list = [
        {
            'name': item['product__name'] or 'Producto sin nombre',
            'quantity': int(item['total_quantity'])
        }
        for item in top_products
    ]
    
    return Response({
        'total_sales': float(total_sales),
        'total_partners': total_partners,
        'total_products': total_products,
        'pending_orders': pending_orders,
        'sales_chart': sales_chart,
        'top_products': top_products_list,
        'last_update': timezone.now().isoformat()
    })


def calculate_percentage_change(current, previous):
    """
    Calcula el cambio porcentual entre dos valores
    """
    if previous == 0:
        return 100 if current > 0 else 0
    
    change = ((current - previous) / previous) * 100
    return round(change, 2)
