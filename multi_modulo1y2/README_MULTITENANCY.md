# Sistema Multitenancy - Módulo 1

## Descripción del Proyecto

Este es un sistema de gestión multitenancy desarrollado en Django que permite a diferentes clínicas (tenants) gestionar sus productos, clientes y usuarios de forma independiente y segura.

## Características Principales

- **Autenticación por Tenant**: Los usuarios se autentican seleccionando su clínica
- **Aislamiento de Datos**: Cada tenant solo puede acceder a sus propios datos
- **Gestión de Productos**: CRUD completo de productos por tenant
- **Gestión de Clientes**: CRUD completo de clientes por tenant
- **Gestión de Usuarios**: Diferentes roles y permisos por tenant
- **Admin de Django**: Interfaz administrativa con filtrado por tenant

## Estructura del Proyecto

```
multi_modulo1y2/
├── multi_tenant_modulo1y2/          # Configuración principal de Django
│   ├── settings.py                  # Configuración del proyecto
│   ├── urls.py                      # URLs principales
│   ├── middleware.py                # Middleware para multitenancy
│   └── wsgi.py                      # Configuración WSGI
├── productos/                       # Aplicación de productos
│   ├── models.py                    # Modelos de productos y tenants
│   ├── views.py                     # Vistas de productos
│   ├── admin.py                     # Configuración del admin
│   └── urls.py                      # URLs de productos
├── clientes/                        # Aplicación de clientes
│   ├── models.py                    # Modelos de clientes y usuarios
│   ├── views.py                     # Vistas de clientes
│   ├── admin.py                     # Configuración del admin
│   └── urls.py                      # URLs de clientes
├── auth_views/                      # Aplicación de autenticación
│   ├── views.py                     # Vistas de login/logout
│   └── urls.py                      # URLs de autenticación
├── templates/                       # Plantillas HTML
│   ├── base/                        # Plantillas base
│   └── login/                       # Plantillas de login
└── manage.py                        # Script de gestión de Django
```

## Modelos Principales

### Tenant
- Representa una clínica o empresa
- Cada tenant tiene un slug único
- Controla el acceso a los datos

### Producto
- Vinculado a un tenant específico
- Incluye nombre, descripción, precio, stock
- Solo visible para usuarios del tenant correspondiente

### Cliente
- Vinculado a un tenant específico
- Información personal y de contacto
- Aislamiento completo por tenant

### UsuarioTenant
- Extiende el modelo User de Django
- Asigna usuarios a tenants específicos
- Diferentes roles (admin, vendedor, cliente)

## Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8+
- Django 5.2+
- MySQL 8.0+
- XAMPP (para entorno de desarrollo)

### 2. Configuración de la Base de Datos
```sql
CREATE DATABASE modulo1y2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Instalación de Dependencias
```bash
cd multi_modulo1y2
pip install -r requirements.txt
```

### 4. Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el Servidor
```bash
python manage.py runserver
```

## Uso del Sistema

### 1. Acceso al Admin
- URL: `http://localhost:8000/admin/`
- Usar las credenciales del superusuario

### 2. Crear Tenants
1. Ir a Admin > Tenants
2. Crear nuevos tenants (ej: Clínica A, Clínica B)
3. Asignar slugs únicos (ej: clinica_a, clinica_b)

### 3. Crear Usuarios por Tenant
1. Crear usuarios en Admin > Users
2. Crear UsuarioTenant vinculando usuario y tenant
3. Asignar roles apropiados

### 4. Acceso al Sistema
- URL: `http://localhost:8000/login/`
- Seleccionar clínica
- Ingresar credenciales
- Acceder solo a datos del tenant

## Seguridad y Aislamiento

### Middleware de Tenant
- Verifica autenticación en cada request
- Filtra datos por tenant del usuario
- Previene acceso cruzado entre tenants

### Filtrado en Admin
- Cada usuario solo ve datos de su tenant
- Filtros automáticos en listas
- Validación en formularios

### Vistas Protegidas
- Decorador `@login_required`
- Verificación de tenant en cada vista
- Redirección automática si no hay acceso

## Personalización

### Agregar Nuevos Modelos
1. Crear modelo en la aplicación correspondiente
2. Agregar campo `tenant` como ForeignKey
3. Configurar admin con filtrado
4. Crear vistas con protección por tenant

### Modificar Templates
- Los templates están en `templates/`
- Usar `{{ tenant.name }}` para mostrar información del tenant
- Extender de `base/base.html` para consistencia

### Agregar Funcionalidades
1. Crear vistas en `views.py`
2. Agregar URLs en `urls.py`
3. Crear templates correspondientes
4. Actualizar middleware si es necesario

## Troubleshooting

### Problemas Comunes

1. **Error de Tenant no encontrado**
   - Verificar que el usuario tenga UsuarioTenant creado
   - Confirmar que el tenant esté activo

2. **Acceso denegado en Admin**
   - Verificar permisos del usuario
   - Confirmar que esté vinculado al tenant correcto

3. **Datos no visibles**
   - Verificar filtros por tenant en el admin
   - Confirmar que los objetos tengan tenant asignado

### Logs y Debugging
- Activar `DEBUG = True` en settings.py
- Revisar consola del servidor
- Verificar logs de Django

## Próximos Pasos

### Funcionalidades Futuras
- Dashboard con gráficos y estadísticas
- API REST para integración externa
- Sistema de notificaciones
- Reportes avanzados por tenant
- Backup automático por tenant

### Mejoras de Seguridad
- Autenticación de dos factores
- Auditoría de acciones
- Encriptación de datos sensibles
- Rate limiting por tenant

## Contacto y Soporte

Para dudas o problemas técnicos:
- Revisar la documentación de Django
- Consultar logs del sistema
- Verificar configuración de la base de datos

---

**Nota**: Este sistema está diseñado para desarrollo y pruebas. Para producción, considerar:
- Configuración de seguridad avanzada
- Optimización de base de datos
- Monitoreo y logging
- Backup y recuperación 