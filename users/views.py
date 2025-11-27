from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer, LoginSerializer, ChangePasswordSerializer
from .permissions import IsAdmin
from audit.mixins import AuditMixin
from audit.models import AuditLog


class RoleViewSet(AuditMixin, viewsets.ModelViewSet):
    """ViewSet para gestión de roles"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    audit_model_name = 'Role'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        return queryset


class UserViewSet(AuditMixin, viewsets.ModelViewSet):
    """ViewSet para gestión de usuarios"""
    queryset = User.objects.select_related('role').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    audit_model_name = 'User'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Debug
        print(f"DEBUG Users: organization={getattr(self.request, 'organization', None)}, user={self.request.user.username}, is_superuser={self.request.user.is_superuser}")
        
        # Filtrar por organización (solo mostrar usuarios con partner en la org actual)
        # Excepto para superusers
        if hasattr(self.request, 'organization') and self.request.organization:
            if not self.request.user.is_superuser:
                # Obtener IDs de usuarios que tienen partner en esta organización
                from partners.models import Partner
                user_ids = list(Partner.objects.all_organizations().filter(
                    organization=self.request.organization
                ).values_list('user_id', flat=True))
                print(f"DEBUG Users: Filtering by user_ids={user_ids}")
                queryset = queryset.filter(id__in=user_ids)
        
        # Filtros
        search = self.request.query_params.get('search', None)
        role = self.request.query_params.get('role', None)
        is_active = self.request.query_params.get('is_active', None)
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role_id=role)
        
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        """Guardar el usuario que creó este registro"""
        instance = serializer.save(created_by=self.request.user)
        self.create_audit_log(AuditLog.CREATE, instance)
        return instance
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def deactivate(self, request, pk=None):
        """Inhabilitar usuario"""
        user = self.get_object()
        if user.id == request.user.id:
            return Response(
                {'error': 'No puedes desactivar tu propio usuario'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_active = False
        user.save()
        self.create_audit_log(
            AuditLog.UPDATE, 
            user, 
            f"Desactivó usuario: {user.username}"
        )
        return Response({'message': 'Usuario desactivado exitosamente'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def activate(self, request, pk=None):
        """Reactivar usuario"""
        user = self.get_object()
        user.is_active = True
        user.save()
        self.create_audit_log(
            AuditLog.UPDATE, 
            user, 
            f"Activó usuario: {user.username}"
        )
        return Response({'message': 'Usuario activado exitosamente'})
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Registrar nuevo usuario"""
        try:
            # Validar datos requeridos
            required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
            for field in required_fields:
                if field not in request.data or not request.data[field]:
                    return Response(
                        {'error': f'El campo {field} es requerido'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Validar que el username no exista
            if User.objects.filter(username=request.data['username']).exists():
                return Response(
                    {'error': 'El nombre de usuario ya existe'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validar que el email no exista
            if User.objects.filter(email=request.data['email']).exists():
                return Response(
                    {'error': 'El email ya está registrado'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Determinar rol según tipo de registro
            register_type = request.data.get('register_type', 'cliente')
            plan = request.data.get('plan', None)
            
            # Obtener rol
            role = None
            try:
                if register_type == 'socio':
                    role = Role.objects.filter(name='SOCIO', is_active=True).first()
                else:
                    role = Role.objects.filter(name='CLIENTE', is_active=True).first()
                
                if not role:
                    role = Role.objects.filter(is_active=True).first()
            except Exception as e:
                print(f"Error al obtener rol: {e}")
            
            # Crear usuario
            user = User.objects.create_user(
                username=request.data['username'],
                email=request.data['email'],
                password=request.data['password'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                role=role
            )
            
            # Crear Partner automáticamente si hay organización
            from partners.models import Partner
            from tenants.models import Organization
            
            org_subdomain = request.headers.get('X-Organization-Subdomain') or request.GET.get('org')
            if org_subdomain:
                try:
                    organization = Organization.objects.get(subdomain=org_subdomain, is_active=True)
                    
                    # Crear partner para este usuario en esta organización
                    Partner.objects.create(
                        user=user,
                        organization=organization,
                        ci=request.data.get('ci', ''),
                        first_name=user.first_name,
                        last_name=user.last_name,
                        email=user.email,
                        phone=request.data.get('phone', ''),
                        address=request.data.get('address', ''),
                        is_active=True
                    )
                    print(f"Partner creado para {user.username} en {organization.name}")
                except Organization.DoesNotExist:
                    print(f"Organización {org_subdomain} no encontrada")
                except Exception as e:
                    print(f"Error al crear partner: {e}")
            
            # Registrar en auditoría
            try:
                from audit.mixins import get_client_ip, get_user_agent
                description = f"Usuario {user.username} se registró como {register_type.upper()}"
                if plan:
                    description += f" con plan {plan}"
                
                AuditLog.objects.create(
                    user=user,
                    action=AuditLog.CREATE,
                    model_name='User',
                    object_id=user.id,
                    description=description,
                    ip_address=get_client_ip(request),
                    user_agent=get_user_agent(request)
                )
            except Exception as e:
                print(f"Error al crear log de auditoría: {e}")
            
            return Response({
                'message': 'Usuario registrado exitosamente',
                'user': UserSerializer(user).data,
                'register_type': register_type,
                'plan': plan
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            print(f"Error en registro: {e}")
            import traceback
            traceback.print_exc()
            return Response(
                {'error': f'Error al registrar usuario: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Iniciar sesión con username o email"""
        from rest_framework_simplejwt.tokens import RefreshToken
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username_or_email = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Intentar encontrar el usuario por username o email
        user = None
        try:
            # Primero intentar por username
            user_obj = User.objects.get(username=username_or_email)
            user = authenticate(username=user_obj.username, password=password)
        except User.DoesNotExist:
            # Si no existe, intentar por email
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is None:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Usuario inactivo'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Validar acceso a la organización en el login
        from tenants.models import Organization
        from partners.models import Partner
        
        org_subdomain = request.headers.get('X-Organization-Subdomain') or request.GET.get('org')
        
        if org_subdomain and not user.is_superuser:
            try:
                organization = Organization.objects.get(subdomain=org_subdomain, is_active=True)
                
                # Si no es ADMIN, validar que tenga partner en esta organización
                is_admin = user.role and user.role.name == 'ADMIN'
                if not is_admin:
                    has_access = Partner.objects.all_organizations().filter(
                        organization=organization,
                        user=user
                    ).exists()
                    
                    if not has_access:
                        # Crear partner automáticamente si no existe
                        try:
                            Partner.objects.create(
                                user=user,
                                organization=organization,
                                ci='',
                                first_name=user.first_name,
                                last_name=user.last_name,
                                email=user.email,
                                phone='',
                                address='',
                                is_active=True
                            )
                            print(f"Partner creado automáticamente para {user.username} en {organization.name}")
                        except Exception as e:
                            print(f"Error al crear partner automático: {e}")
                            return Response(
                                {'error': 'Acceso denegado',
                                 'detail': f'No tienes acceso a {organization.name}'},
                                status=status.HTTP_403_FORBIDDEN
                            )
            except Organization.DoesNotExist:
                return Response(
                    {'error': 'Organización no encontrada'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        login(request, user)
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Registrar login en auditoría (opcional si no hay organización)
        try:
            from audit.mixins import get_client_ip, get_user_agent
            AuditLog.objects.create(
                user=user,
                action=AuditLog.LOGIN,
                description=f"Usuario {user.username} inició sesión",
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request)
            )
        except Exception as e:
            # Si falla el log de auditoría, continuar igual
            print(f"Error logging audit: {e}")
        
        return Response({
            'message': 'Inicio de sesión exitoso',
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token
        })
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Cerrar sesión"""
        user = request.user
        username = user.username if user.is_authenticated else 'unknown'
        
        # Registrar logout en auditoría antes de cerrar sesión (opcional)
        try:
            from audit.mixins import get_client_ip, get_user_agent
            AuditLog.objects.create(
                user=user,
                action=AuditLog.LOGOUT,
                description=f"Usuario {username} cerró sesión",
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request)
            )
        except Exception as e:
            print(f"Error logging audit: {e}")
        
        logout(request)
        return Response({'message': 'Sesión cerrada exitosamente'})
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Obtener información del usuario actual"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario actual"""
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'error': 'Contraseña actual incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Contraseña cambiada exitosamente'})
