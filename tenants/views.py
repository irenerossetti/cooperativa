from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.authentication import SessionAuthentication
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Organization, OrganizationMember
from .serializers import (
    OrganizationSerializer,
    OrganizationRegistrationSerializer,
    OrganizationMemberSerializer
)
from users.models import User


# Custom SessionAuthentication sin CSRF para super admin
class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # No enforce CSRF


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        # Obtener solo las organizaciones donde el usuario es miembro
        return Organization.objects.filter(
            members__user=user,
            members__is_active=True
        ).distinct()
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Obtiene la organización actual del request"""
        organization = getattr(request, 'organization', None)
        if not organization:
            return Response(
                {'error': 'No hay organización activa en el contexto actual'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(organization)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Lista los miembros de una organización"""
        organization = self.get_object()
        members = OrganizationMember.objects.filter(organization=organization)
        serializer = OrganizationMemberSerializer(members, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Agrega un miembro a la organización"""
        organization = self.get_object()
        
        # Verificar que el usuario actual sea owner o admin
        membership = OrganizationMember.objects.filter(
            organization=organization,
            user=request.user,
            role__in=['OWNER', 'ADMIN']
        ).first()
        
        if not membership:
            return Response(
                {'error': 'No tienes permisos para agregar miembros'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrganizationMemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_organization(request):
    """
    Endpoint público para registrar una nueva organización.
    Crea la organización y el usuario propietario.
    """
    serializer = OrganizationRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        result = serializer.save()
        
        return Response({
            'message': 'Organización registrada exitosamente',
            'organization': {
                'id': result['organization'].id,
                'name': result['organization'].name,
                'subdomain': result['organization'].subdomain,
                'plan': result['organization'].plan,
                'status': result['organization'].status,
            },
            'user': {
                'id': result['user'].id,
                'username': result['user'].username,
                'email': result['user'].email,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_organizations(request):
    """Lista las organizaciones del usuario autenticado"""
    memberships = OrganizationMember.objects.filter(
        user=request.user,
        is_active=True
    ).select_related('organization')
    
    organizations = []
    for membership in memberships:
        org = membership.organization
        organizations.append({
            'id': org.id,
            'name': org.name,
            'subdomain': org.subdomain,
            'plan': org.plan,
            'status': org.status,
            'role': membership.role,
            'is_active': org.is_active,
        })
    
    return Response(organizations)



# ============================================
# SUPER ADMIN VIEWS
# ============================================

class IsSuperAdmin(IsAuthenticated):
    """Permiso personalizado para super admins"""
    def has_permission(self, request, view):
        return (
            super().has_permission(request, view) and 
            request.user.is_superuser
        )


@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def super_admin_dashboard_stats(request):
    """
    Estadísticas globales para el dashboard de super admin
    """
    # Estadísticas de organizaciones
    total_orgs = Organization.objects.count()
    active_orgs = Organization.objects.filter(status='ACTIVE').count()
    trial_orgs = Organization.objects.filter(status='TRIAL').count()
    suspended_orgs = Organization.objects.filter(status='SUSPENDED').count()
    
    # Estadísticas de usuarios
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Organizaciones por plan
    orgs_by_plan = Organization.objects.values('plan').annotate(count=Count('id'))
    plan_distribution = {item['plan']: item['count'] for item in orgs_by_plan}
    
    # Nuevas organizaciones (últimos 30 días)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_orgs_last_month = Organization.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    
    # Organizaciones recientes
    recent_orgs = Organization.objects.order_by('-created_at')[:5]
    recent_orgs_data = [{
        'id': org.id,
        'name': org.name,
        'subdomain': org.subdomain,
        'plan': org.plan,
        'status': org.status,
        'created_at': org.created_at,
        'members_count': org.members.count()
    } for org in recent_orgs]
    
    return Response({
        'organizations': {
            'total': total_orgs,
            'active': active_orgs,
            'trial': trial_orgs,
            'suspended': suspended_orgs,
            'new_last_month': new_orgs_last_month
        },
        'users': {
            'total': total_users,
            'active': active_users
        },
        'plan_distribution': plan_distribution,
        'recent_organizations': recent_orgs_data
    })


@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def super_admin_list_organizations(request):
    """
    Lista todas las organizaciones con filtros y búsqueda
    """
    queryset = Organization.objects.all()
    
    # Filtros
    status_filter = request.GET.get('status')
    plan_filter = request.GET.get('plan')
    search = request.GET.get('search')
    
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    if plan_filter:
        queryset = queryset.filter(plan=plan_filter)
    
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(subdomain__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Anotar con conteo de miembros
    queryset = queryset.annotate(
        members_count=Count('members')
    ).order_by('-created_at')
    
    # Serializar
    organizations = []
    for org in queryset:
        organizations.append({
            'id': org.id,
            'name': org.name,
            'subdomain': org.subdomain,
            'email': org.email,
            'phone': org.phone,
            'plan': org.plan,
            'plan_display': org.get_plan_display_name(),
            'status': org.status,
            'is_active': org.is_active,
            'members_count': org.members_count,
            'max_users': org.max_users,
            'created_at': org.created_at,
            'trial_ends_at': org.trial_ends_at,
            'subscription_ends_at': org.subscription_ends_at
        })
    
    return Response(organizations)


@api_view(['GET'])
@permission_classes([IsSuperAdmin])
def super_admin_organization_detail(request, org_id):
    """
    Detalle completo de una organización
    """
    try:
        org = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return Response(
            {'error': 'Organización no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Obtener miembros
    members = OrganizationMember.objects.filter(
        organization=org
    ).select_related('user')
    
    members_data = [{
        'id': member.id,
        'user_id': member.user.id,
        'username': member.user.username,
        'email': member.user.email,
        'full_name': member.user.get_full_name(),
        'role': member.role,
        'is_active': member.is_active,
        'joined_at': member.joined_at
    } for member in members]
    
    return Response({
        'id': org.id,
        'name': org.name,
        'slug': org.slug,
        'subdomain': org.subdomain,
        'email': org.email,
        'phone': org.phone,
        'address': org.address,
        'plan': org.plan,
        'plan_display': org.get_plan_display_name(),
        'status': org.status,
        'is_active': org.is_active,
        'max_users': org.max_users,
        'max_products': org.max_products,
        'max_storage_mb': org.max_storage_mb,
        'created_at': org.created_at,
        'updated_at': org.updated_at,
        'trial_ends_at': org.trial_ends_at,
        'subscription_ends_at': org.subscription_ends_at,
        'settings': org.settings,
        'members': members_data,
        'members_count': len(members_data)
    })


@api_view(['PUT'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsSuperAdmin])
def super_admin_update_organization(request, org_id):
    """
    Actualizar una organización (plan, estado, límites, etc.)
    """
    try:
        org = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return Response(
            {'error': 'Organización no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Actualizar campos permitidos
    allowed_fields = [
        'name', 'email', 'phone', 'address', 'plan', 'status',
        'is_active', 'max_users', 'max_products', 'max_storage_mb',
        'trial_ends_at', 'subscription_ends_at'
    ]
    
    for field in allowed_fields:
        if field in request.data:
            setattr(org, field, request.data[field])
    
    org.save()
    
    return Response({
        'message': 'Organización actualizada exitosamente',
        'organization': {
            'id': org.id,
            'name': org.name,
            'plan': org.plan,
            'status': org.status,
            'is_active': org.is_active
        }
    })


@api_view(['DELETE'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsSuperAdmin])
def super_admin_delete_organization(request, org_id):
    """
    Eliminar una organización (soft delete - desactivar)
    """
    try:
        org = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return Response(
            {'error': 'Organización no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Soft delete
    org.is_active = False
    org.status = 'CANCELLED'
    org.save()
    
    return Response({
        'message': f'Organización {org.name} desactivada exitosamente'
    })


@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([IsSuperAdmin])
def super_admin_create_organization(request):
    """
    Crear una nueva organización desde el panel de super admin
    """
    serializer = OrganizationRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        result = serializer.save()
        
        return Response({
            'message': 'Organización creada exitosamente',
            'organization': {
                'id': result['organization'].id,
                'name': result['organization'].name,
                'subdomain': result['organization'].subdomain,
                'plan': result['organization'].plan,
                'status': result['organization'].status,
            },
            'user': {
                'id': result['user'].id,
                'username': result['user'].username,
                'email': result['user'].email,
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
