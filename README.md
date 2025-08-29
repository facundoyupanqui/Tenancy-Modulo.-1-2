# Tenancy Módulo 1 y 2

Proyecto Django multi-tenant con base de datos MySQL. Sistema modular para gestión de productos y clientes con aislamiento por tenant.

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```sh
git clone <URL_DEL_REPOSITORIO>
cd Tenancy-Modulo.-1-2/multi_modulo1y2
```

### 2. Crear y activar entorno virtual
```sh
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```sh
pip install -r requirements.txt
```

### 4. Base de datos MySQL

El proyecto utiliza MySQL como base de datos. Asegúrate de tener MySQL instalado y configurado.

**Configuración de la base de datos:**
- **Base de datos:** `modulo1y2`
- **Usuario:** `alee`
- **Contraseña:** `1234`
- **Host:** `localhost`
- **Puerto:** `3306`

**Crear la base de datos:**
```sql
CREATE DATABASE modulo1y2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Aplicar migraciones
```sh
python manage.py check
```

### 6. Crear usuario administrador
```sh
python manage.py createsuperuser
```

### 7. Ejecutar el servidor de desarrollo
```sh
python manage.py runserver
```

Accede a [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) para el panel de administración.

---

## 📁 Estructura del Proyecto

```
multi_modulo1y2/
│   manage.py
│   requirements.txt
│
├───multi_modulo1y2/
│   │   __init__.py
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   middleware.py
│   │
│   ├───auth_views/           # Gestión de autenticación
│   │   │   __init__.py
│   │   │   apps.py
│   │   │   urls.py
│   │   │   views.py
│   │
│   ├───clientes/             # Gestión de clientes
│   │   │   __init__.py
│   │   │   admin.py
│   │   │   apps.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   tests.py
│   │   │   urls.py
│   │   │   views.py
│   │
│   ├───productos/            # Gestión de productos y tenants
│   │   │   __init__.py
│   │   │   admin.py
│   │   │   apps.py
│   │   │   forms.py
│   │   │   models.py
│   │   │   tests.py
│   │   │   urls.py
│   │   │   views.py
│   │
│   ├───templates/            # Plantillas HTML
│   │   ├───base/
│   │   └───login/
│   │
│   └───users/                # Gestión de usuarios
│       │   __init__.py
│       │   admin.py
│       │   apps.py
│       │   forms.py
│       │   models.py
│       │   tests.py
│       │   urls.py
│       │   views.py
```

---

## 📝 Notas

- El proyecto utiliza MySQL como base de datos para mayor robustez y escalabilidad.
- El sistema implementa un modelo multi-tenant donde cada usuario pertenece a un tenant específico.
- Los productos y clientes están aislados por tenant, asegurando que cada usuario solo pueda ver y gestionar los datos de su propio tenant.

---

## 📚 Documentación

- [Documentación oficial de Django](https://docs.djangoproject.com/en/5.2/)
- [Documentación oficial de MySQL](https://dev.mysql.com/doc/)

---

## 🛠️ Requerimientos

Ver archivo `requirements.txt`.

## 🔑 Funcionalidades

### Sistema Multi-Tenant
- Aislamiento de datos por tenant
- Middleware para gestión de contexto de tenant
- Filtrado automático de consultas por tenant

### Gestión de Productos
- Listado, creación, edición y eliminación de productos
- Filtrado automático por tenant
- Admin personalizado con filtrado por tenant

### Gestión de Clientes
- Listado, creación, edición y eliminación de clientes
- Filtrado automático por tenant
- Admin personalizado con filtrado por tenant

### Gestión de Tenants (Clínicas)
- Creación y gestión de clínicas
- Admin personalizado con control de acceso

### Autenticación
- Login, logout y registro de usuarios
- Asignación automática de tenant
- Validación de acceso por tenant

---

## 🧪 Datos de Prueba

El sistema incluye datos de prueba preconfigurados:

### Clínicas (Tenants)
- **Clínica A**: Dirección de Clínica A, Ciudad A
- **Clínica B**: Dirección de Clínica B, Ciudad B

### Usuarios de Prueba
- **Clínica A**: 
  - `admin_clinica_a` (Admin) - Contraseña: `test123`
  - `vendedor_clinica_a` (Vendedor) - Contraseña: `test123`
- **Clínica B**: 
  - `admin_clinica_b` (Admin) - Contraseña: `test123`
  - `vendedor_clinica_b` (Vendedor) - Contraseña: `test123`

### Superusuario
- **Usuario**: `admin`
- **Contraseña**: `admin123`

---

## 🔒 Características de Seguridad

- **Aislamiento total**: Cada tenant solo ve sus propios datos
- **Validación de tenant**: Middleware verifica que el usuario tenga tenant asignado
- **Prevención de cambio de tenant**: Los usuarios no pueden modificar su tenant
- **Filtrado automático**: Todas las consultas se filtran por tenant automáticamente
- **Control de acceso**: Solo superusuarios pueden ver todos los tenants

---

## Licencia

Este proyecto está bajo la licencia MIT.