# Sistema Multi-Tenant Integrado (Módulos 1 y 2)

Este proyecto es una integración de los módulos 1 y 2 del sistema multi-tenant, combinando la gestión de productos y clientes en un único sistema con autenticación centralizada y filtrado por tenant.

## Características

- **Sistema Multi-Tenant**: Separación completa de datos entre diferentes tenants (clínicas)
- **Autenticación por Tenant**: Los usuarios solo pueden acceder a los datos de su tenant asignado
- **Middleware de Filtrado**: Filtrado automático de consultas por tenant
- **Gestión de Productos**: Catálogo de productos por tenant
- **Gestión de Clientes**: Registro y seguimiento de clientes por tenant

## Estructura del Proyecto

```
multi_modulo1y2/
├── auth_views/         # Vistas de autenticación
├── clientes/           # Aplicación de gestión de clientes
├── multi_tenant_modulo1y2/  # Configuración principal del proyecto
│   ├── middleware.py   # Middleware para filtrado por tenant
│   ├── settings.py     # Configuración del proyecto
│   └── urls.py         # URLs principales
├── productos/          # Aplicación de gestión de productos y tenants
├── templates/          # Plantillas HTML
│   ├── base/           # Plantillas base
│   └── login/          # Plantillas de autenticación
└── users/              # Aplicación de gestión de usuarios
```

## Modelos Principales

### Tenant (productos/models.py)

Modelo central que representa cada tenant (clínica) en el sistema:

- **name**: Nombre del tenant
- **slug**: Identificador único para URLs
- **is_active**: Estado del tenant
- **created_at**: Fecha de creación

### CustomUser (users/models.py)

Extensión del modelo de usuario de Django con relación al tenant:

- **tenant**: Relación con el tenant al que pertenece
- **rol**: Rol del usuario en el sistema
- **is_active**: Estado del usuario
- **created_at**: Fecha de creación

### Producto (productos/models.py)

Productos asociados a cada tenant:

- **tenant**: Relación con el tenant
- **nombre**, **descripcion**, **precio**, **stock**: Información del producto
- **categoria**: Categoría del producto
- **is_active**: Estado del producto
- **created_at**, **updated_at**: Fechas de creación y actualización

### Cliente (clientes/models.py)

Clientes asociados a cada tenant:

- **tenant**: Relación con el tenant
- **nombre**, **apellido**, **email**, **telefono**, **direccion**: Información del cliente
- **fecha_nacimiento**: Fecha de nacimiento del cliente
- **is_active**: Estado del cliente
- **created_at**, **updated_at**: Fechas de creación y actualización

## Middleware

El sistema utiliza dos middleware principales:

1. **TenantMiddleware**: Gestiona la selección de tenant y el acceso a las rutas
2. **TenantFilterMiddleware**: Filtra automáticamente las consultas por tenant

## Autenticación

El sistema de autenticación incluye:

- **Login con selección de tenant**: Los usuarios deben seleccionar su tenant al iniciar sesión
- **Registro con asignación de tenant**: Los nuevos usuarios se asignan a un tenant específico
- **Validación de acceso**: Se verifica que el usuario tenga acceso al tenant seleccionado

## Instalación y Configuración

1. Clonar el repositorio
2. Instalar dependencias: `pip install -r requirements.txt`
3. Configurar la base de datos en `settings.py`
4. Ejecutar migraciones: `python manage.py migrate`
5. Crear un superusuario: `python manage.py createsuperuser`
6. Iniciar el servidor: `python manage.py runserver`

## Uso

1. Acceder a la página de inicio: `http://localhost:8000/`
2. Iniciar sesión con un usuario existente o registrar uno nuevo
3. Seleccionar el tenant al que se desea acceder
4. Navegar por las diferentes secciones del sistema