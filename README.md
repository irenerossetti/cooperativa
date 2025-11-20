# Backend - Sistema de Gestión de Cooperativa

Backend desarrollado con Django REST Framework para la gestión de una cooperativa agrícola.

## Estructura del Proyecto

```
Backend/
├── config/              # Configuración del proyecto Django
├── users/              # Gestión de usuarios, roles y autenticación
├── partners/           # Gestión de socios y comunidades
├── parcels/            # Gestión de parcelas, tipos de suelo y cultivos
├── audit/              # Bitácora de auditoría
└── core/               # Utilidades compartidas
```

## Instalación

1. Crear y activar entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno en `.env`:
```
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key
DEBUG=True
```

4. Ejecutar migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Inicializar roles del sistema:
```bash
python manage.py init_roles
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecutar servidor:
```bash
python manage.py runserver
```

## API Endpoints

### Autenticación
- `POST /api/auth/users/login/` - Iniciar sesión
- `POST /api/auth/users/logout/` - Cerrar sesión
- `GET /api/auth/users/me/` - Información del usuario actual
- `POST /api/auth/users/change_password/` - Cambiar contraseña

### Usuarios
- `GET /api/auth/users/` - Listar usuarios
- `POST /api/auth/users/` - Crear usuario
- `GET /api/auth/users/{id}/` - Detalle de usuario
- `PUT /api/auth/users/{id}/` - Actualizar usuario
- `DELETE /api/auth/users/{id}/` - Eliminar usuario
- `POST /api/auth/users/{id}/deactivate/` - Inhabilitar usuario
- `POST /api/auth/users/{id}/activate/` - Reactivar usuario

### Roles
- `GET /api/auth/roles/` - Listar roles
- `POST /api/auth/roles/` - Crear rol
- `GET /api/auth/roles/{id}/` - Detalle de rol
- `PUT /api/auth/roles/{id}/` - Actualizar rol

### Socios
- `GET /api/partners/partners/` - Listar socios
- `POST /api/partners/partners/` - Crear socio
- `GET /api/partners/partners/{id}/` - Detalle de socio
- `PUT /api/partners/partners/{id}/` - Actualizar socio
- `DELETE /api/partners/partners/{id}/` - Eliminar socio
- `POST /api/partners/partners/{id}/deactivate/` - Inhabilitar socio
- `POST /api/partners/partners/{id}/activate/` - Reactivar socio

### Comunidades
- `GET /api/partners/communities/` - Listar comunidades
- `POST /api/partners/communities/` - Crear comunidad

### Parcelas
- `GET /api/parcels/parcels/` - Listar parcelas
- `POST /api/parcels/parcels/` - Crear parcela
- `GET /api/parcels/parcels/{id}/` - Detalle de parcela
- `PUT /api/parcels/parcels/{id}/` - Actualizar parcela

### Tipos de Suelo y Cultivos
- `GET /api/parcels/soil-types/` - Listar tipos de suelo
- `GET /api/parcels/crops/` - Listar cultivos

### Auditoría
- `GET /api/audit/logs/` - Listar registros de auditoría

## Filtros Disponibles

### Usuarios
- `?search=texto` - Buscar por username, email, nombre
- `?role=id` - Filtrar por rol
- `?is_active=true/false` - Filtrar por estado

### Socios
- `?search=texto` - Buscar por CI, nombre, email, teléfono
- `?community=id` - Filtrar por comunidad
- `?status=ACTIVE/INACTIVE/SUSPENDED` - Filtrar por estado

### Parcelas
- `?partner=id` - Filtrar por socio
- `?soil_type=id` - Filtrar por tipo de suelo
- `?crop=id` - Filtrar por cultivo
- `?status=ACTIVE/INACTIVE` - Filtrar por estado

## Características Implementadas

✅ Autenticación y gestión de sesiones
✅ Gestión de usuarios con roles y permisos
✅ CRUD de socios con validaciones (CI/NIT únicos)
✅ CRUD de parcelas por socio
✅ Búsquedas y filtros avanzados
✅ Bitácora de auditoría automática
✅ Validación de datos en formularios
✅ Prevención de duplicados
✅ Modelo de datos en PostgreSQL

## Tecnologías

- Django 4.2
- Django REST Framework
- PostgreSQL (Neon)
- python-dotenv
- dj-database-url
- django-cors-headers
