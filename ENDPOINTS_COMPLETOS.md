# 📋 Lista Completa de Endpoints - API REST

## Total: 200+ Endpoints

---

## 🔐 Autenticación (users)

### Sesión
```
POST   /api/auth/users/login/                         - Iniciar sesión
POST   /api/auth/users/logout/                        - Cerrar sesión
GET    /api/auth/users/me/                            - Usuario actual
POST   /api/auth/users/change_password/               - Cambiar contraseña
```

### Usuarios
```
GET    /api/auth/users/                               - Listar usuarios
POST   /api/auth/users/                               - Crear usuario
GET    /api/auth/users/{id}/                          - Detalle de usuari