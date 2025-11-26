# 📝 CHEAT SHEET - Demostración Multi-Tenant

## 🚀 INICIO RÁPIDO

### 1. Iniciar servidor:
```bash
cd Backend
python manage.py runserver
```

### 2. URL para registrar:
```
http://127.0.0.1:8000/api/tenants/register/
```

---

## 📋 JSON PARA COPIAR Y PEGAR

```json
{
    "organization_name": "Cooperativa Santa Rosa",
    "subdomain": "santarosa",
    "email": "contacto@santarosa.com",
    "phone": "+591 3 5551234",
    "username": "adminsantarosa",
    "user_email": "admin@santarosa.com",
    "password": "santarosa123",
    "first_name": "Carlos",
    "last_name": "Mendoza"
}
```

**Alternativa 2:**
```json
{
    "organization_name": "Cooperativa El Porvenir",
    "subdomain": "porvenir",
    "email": "info@porvenir.com",
    "phone": "+591 3 7778888",
    "username": "adminporvenir",
    "user_email": "admin@porvenir.com",
    "password": "porvenir123",
    "first_name": "María",
    "last_name": "López"
}
```

---

## 🔗 URLs IMPORTANTES

### Registrar organización:
```
http://127.0.0.1:8000/api/tenants/register/
```

### Ver socios de Santa Rosa:
```
http://127.0.0.1:8000/api/partners/?org=santarosa
```

### Ver socios de San Juan (comparación):
```
http://127.0.0.1:8000/api/partners/?org=sanjuan
```

### Admin Django:
```
http://127.0.0.1:8000/admin/
Usuario: admin
Password: admin123
```

### Login frontend:
```
http://localhost:5173/login?org=santarosa
```

---

## 🎯 PASOS DE LA DEMO

1. ✅ Abrir URL de registro
2. ✅ Pegar JSON en el campo "Content"
3. ✅ Click en botón "POST"
4. ✅ Mostrar respuesta exitosa
5. ✅ Abrir URL con ?org=santarosa
6. ✅ Comparar con ?org=sanjuan
7. ✅ Mostrar en Admin Django

---

## 💬 FRASES CLAVE

**Al inicio:**
> "Voy a demostrar cómo registrar una nueva cooperativa en nuestro sistema multi-tenant."

**Durante registro:**
> "Cada cooperativa tiene su subdominio único y usuario administrador."

**Mostrando aislamiento:**
> "Los datos están completamente aislados. Santa Rosa no puede ver datos de San Juan."

**Al final:**
> "Esto permite que múltiples cooperativas usen la misma aplicación con datos separados."

---

## 🆘 SOLUCIONES RÁPIDAS

### Si falla el registro:
```bash
python crear_organizacion_demo.py
```

### Si el servidor no responde:
```bash
Ctrl+C
python manage.py runserver
```

### Si hay error de subdominio duplicado:
Cambiar `"subdomain": "santarosa2"`

---

## 📊 DATOS PARA MENCIONAR

- **Planes**: FREE (5 usuarios), BASIC (10), PROFESSIONAL (20), ENTERPRISE (ilimitado)
- **Aislamiento**: 100% separación de datos
- **Acceso**: Subdominio, Header HTTP, o Query parameter
- **Seguridad**: Filtros automáticos en base de datos

---

## ⏱️ TIMING

- Preparación: 2 min
- Registro: 3 min
- Demostración aislamiento: 2 min
- Admin Django: 2 min
- **Total: 10 minutos**

---

## 🎬 SCRIPT ULTRA-CORTO

1. "Voy a registrar Cooperativa Santa Rosa"
2. [Pegar JSON y POST]
3. "Organización creada con plan FREE"
4. "Veamos sus datos aislados"
5. [Mostrar ?org=santarosa vacío]
6. [Mostrar ?org=sanjuan con datos]
7. "Datos completamente separados"
8. [Mostrar en Admin]
9. "Sistema listo para múltiples cooperativas"

---

## ✅ CHECKLIST

- [ ] Servidor corriendo
- [ ] JSON copiado
- [ ] URLs abiertas en pestañas
- [ ] Admin login listo
- [ ] Script de respaldo listo

---

## 🔥 BACKUP PLAN

Si TODO falla:
1. Mostrar organizaciones existentes en Admin
2. Explicar el concepto con las que ya existen
3. Mostrar aislamiento con sanjuan vs progreso
4. Ejecutar `python crear_organizacion_demo.py` después

---

¡ÉXITO EN TU DEMO! 🚀
