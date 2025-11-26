from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Organization, OrganizationMember
from .serializers import (
    OrganizationSerializer,
    OrganizationRegistrationSerializer,
    OrganizationMemberSerializer
)


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
