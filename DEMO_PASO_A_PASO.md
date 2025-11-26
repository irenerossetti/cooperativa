# 🎯 DEMOSTRACIÓN: Registrar una Organización - PASO A PASO

## 📋 Preparación (antes de la demo)

### 1. Asegúrate de que el servidor esté corriendo:

```bash
# En una terminal, en la carpeta Backend:
python manage.py runserver
```

**Debes ver:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## 🎬 DEMOSTRACIÓN EN VIVO

### PASO 1: Abrir el navegador

1. Abre tu navegador (Chrome, Firefox, Edge)
2. Ve a esta URL:
```
http://127.0.0.1:8000/api/tenants/register/
```

**Lo que verás:**
- Una página de Django REST Framework
- Título: "Register Organization"
- Un formulario con un área de texto grande

---

### PASO 2: Preparar los datos

**Di a tu audiencia:**
> "Voy a registrar una nueva cooperativa en el sistema. Cada cooperativa tendrá sus propios datos completamente aislados."

**Copia este JSON** (puedes cambiar los valores):

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

**Explica cada campo:**
- `organization_name`: Nombre de la cooperativa
- `subdomain`: Identificador único (solo minúsculas, sin espacios)
- `email`: Email de contacto de la cooperativa
- `phone`: Teléfono de contacto
- `username`: Usuario administrador que se creará
- `user_email`: Email del administrador
- `password`: Contraseña del administrador
- `first_name` y `last_name`: Nombre del administrador

---

### PASO 3: Registrar la organización

1. **Baja en la página** hasta encontrar el campo grande que dice "Content:"

2. **Pega el JSON** en ese campo

3. **Haz clic en el botón azul "POST"** (abajo a la derecha)

4. **Espera 1-2 segundos**

---

### PASO 4: Ver el resultado

**Si todo salió bien, verás:**

```json
{
    "message": "Organización registrada exitosamente",
    "organization": {
        "id": 6,
        "name": "Cooperativa Santa Rosa",
        "subdomain": "santarosa",
        "plan": "FREE",
        "status": "TRIAL"
    },
    "user": {
        "id": 21,
        "username": "adminsantarosa",
        "email": "admin@santarosa.com"
    }
}
```

**Explica a tu audiencia:**
> "¡Listo! La cooperativa ha sido registrada. Ahora tiene:
> - Su propia organización con ID único
> - Un plan FREE de prueba por 30 días
> - Un usuario administrador creado automáticamente
> - Su propio subdominio: 'santarosa'"

---

### PASO 5: Demostrar el aislamiento de datos

**Ahora demuestra que los datos están aislados:**

1. **Abre una nueva pestaña** y ve a:
```
http://127.0.0.1:8000/api/partners/?org=santarosa
```

**Explica:**
> "Esta es la lista de socios de Santa Rosa. Está vacía porque es una organización nueva."

2. **Abre otra pestaña** y ve a:
```
http://127.0.0.1:8000/api/partners/?org=sanjuan
```

**Explica:**
> "Esta es la lista de socios de San Juan (otra cooperativa). Tiene sus propios datos. Las organizaciones están completamente aisladas."

---

### PASO 6: Verificar en el Admin de Django

1. **Ve a:**
```
http://127.0.0.1:8000/admin/
```

2. **Haz login** con:
   - Usuario: `admin`
   - Password: `admin123`

3. **Haz clic en "Organizations"** (en la sección TENANTS)

4. **Muestra la lista** de organizaciones

**Explica:**
> "Aquí podemos ver todas las cooperativas registradas en el sistema. Cada una tiene su plan, estado, y límites configurados."

---

## 🎯 PUNTOS CLAVE PARA MENCIONAR

### 1. Multi-Tenancy (SaaS)
> "Este es un sistema multi-tenant, lo que significa que múltiples cooperativas pueden usar la misma aplicación, pero cada una tiene sus datos completamente separados."

### 2. Registro Automático
> "El proceso de registro crea automáticamente:
> - La organización
> - El usuario administrador
> - La membresía (relación entre usuario y organización)
> - Todo en una sola operación"

### 3. Planes y Límites
> "Cada organización tiene un plan que define límites:
> - FREE: 5 usuarios, 100 productos
> - BASIC: 10 usuarios, 500 productos
> - PROFESSIONAL: 20 usuarios, 1000 productos
> - ENTERPRISE: Ilimitado"

### 4. Aislamiento de Datos
> "Los datos están completamente aislados. Una cooperativa no puede ver ni acceder a los datos de otra. Esto se logra mediante:
> - Middleware que detecta la organización actual
> - Filtros automáticos en todas las consultas a la base de datos
> - Validaciones de seguridad"

### 5. Acceso Flexible
> "Las organizaciones pueden acceder al sistema de 3 formas:
> 1. Subdominio: santarosa.tuapp.com
> 2. Header HTTP: X-Organization-Subdomain: santarosa
> 3. Query parameter: ?org=santarosa"

---

## 🔄 SI ALGO SALE MAL

### Error: "Este subdominio ya está en uso"
**Solución:** Cambia el `subdomain` a otro valor único
```json
"subdomain": "santarosa2"
```

### Error: "Este nombre de usuario ya está en uso"
**Solución:** Cambia el `username`
```json
"username": "adminsantarosa2"
```

### Error: "Este email ya está registrado"
**Solución:** Cambia el `user_email`
```json
"user_email": "admin2@santarosa.com"
```

### Error: "La contraseña es muy corta"
**Solución:** Usa una contraseña de al menos 8 caracteres
```json
"password": "password123"
```

---

## 📊 DEMOSTRACIÓN ADICIONAL (Opcional)

### Mostrar que el usuario puede hacer login:

1. **Ve al frontend:**
```
http://localhost:5173/login?org=santarosa
```

2. **Haz login con:**
   - Usuario: `adminsantarosa`
   - Password: `santarosa123`

3. **Muestra el dashboard**

**Explica:**
> "El usuario administrador puede hacer login y empezar a usar el sistema inmediatamente. Todo lo que cree (productos, socios, ventas) quedará asociado a su organización."

---

## 🎬 SCRIPT COMPLETO PARA LA DEMO

**Inicio:**
> "Hoy voy a demostrar cómo funciona el sistema multi-tenant que hemos implementado. Voy a registrar una nueva cooperativa desde cero."

**Durante el registro:**
> "Estoy completando los datos de la cooperativa: nombre, subdominio único, email de contacto, y los datos del usuario administrador que se creará automáticamente."

**Después del registro:**
> "Como pueden ver, la organización se creó exitosamente. Ahora tiene su propio espacio en el sistema, completamente aislado de las demás cooperativas."

**Mostrando el aislamiento:**
> "Aquí vemos que cada organización tiene sus propios datos. Santa Rosa no puede ver los datos de San Juan, y viceversa. Esto garantiza la privacidad y seguridad de cada cooperativa."

**Cierre:**
> "Este sistema permite que múltiples cooperativas usen la misma aplicación, reduciendo costos de infraestructura y mantenimiento, mientras mantiene sus datos completamente separados y seguros."

---

## ✅ CHECKLIST PRE-DEMO

- [ ] Servidor backend corriendo (`python manage.py runserver`)
- [ ] Navegador abierto
- [ ] JSON de ejemplo copiado y listo para pegar
- [ ] Credenciales de admin anotadas (admin/admin123)
- [ ] URLs importantes anotadas
- [ ] Entender los conceptos clave (multi-tenancy, aislamiento, planes)

---

## 🎯 TIEMPO ESTIMADO

- Preparación: 2 minutos
- Demostración: 5-7 minutos
- Preguntas: 3-5 minutos
- **Total: 10-15 minutos**

---

## 💡 TIPS PARA LA DEMO

1. **Practica antes** al menos 2 veces
2. **Ten el JSON listo** en un archivo de texto
3. **Explica mientras haces** cada paso
4. **Muestra confianza** - si algo falla, usa el script de respaldo
5. **Prepara respuestas** para preguntas comunes

---

## 🚀 SCRIPT DE RESPALDO (Si falla la demo en vivo)

Si por alguna razón la demo en vivo falla, ejecuta:

```bash
python crear_organizacion_demo.py
```

Y di:
> "También tenemos un script automatizado que puede crear organizaciones. Esto es útil para migraciones masivas o configuraciones iniciales."

Luego muestra el resultado del script y continúa con la demostración del aislamiento de datos.

---

## 📞 PREGUNTAS FRECUENTES

**P: ¿Cuántas organizaciones puede soportar el sistema?**
R: Técnicamente ilimitadas. Depende de la infraestructura del servidor.

**P: ¿Qué pasa si una organización quiere cambiar de plan?**
R: El administrador del sistema puede cambiar el plan desde el admin de Django, y los límites se actualizan automáticamente.

**P: ¿Los datos están realmente aislados?**
R: Sí, completamente. Usamos filtros automáticos a nivel de base de datos que garantizan que cada organización solo vea sus propios datos.

**P: ¿Se puede eliminar una organización?**
R: Sí, desde el admin de Django. Al eliminar una organización, se eliminan todos sus datos asociados.

**P: ¿Cómo se cobra a las organizaciones?**
R: El siguiente paso es integrar una pasarela de pagos (Stripe/PayPal) para cobros automáticos mensuales según el plan.

---

¡BUENA SUERTE CON TU DEMOSTRACIÓN! 🎉
