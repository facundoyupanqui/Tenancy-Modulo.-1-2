# README — Multitenancy y Django Admin (Proyecto Clínica)

> Última actualización: 27 de agosto de 2025
>
> Autor: Equipo de Desarrollo

---

## Resumen
Este repositorio contiene la implementación del **Módulo Multitenant** orientado a clínicas y la **configuración del Django Admin** para que respete la separación por tenants. El objetivo principal es que cada usuario, registro y operación permanezcan aislados por *tenant* (una `Clinic`) y que **usuarios de una clínica no puedan ver ni modificar datos de otra**.

Se implementaron las piezas claves:
- Modelo `Clinic` (tenant).
- Extensión del modelo de usuario (`User`) con campo `tenant` y manager personalizado para forzar la creación con tenant.
- Mixin reusable `TenantAdminMixin` que restringe listas, formularios, FKs, inlines y permisos en el Django Admin.
- Adaptaciones en `admin.py` para `Cliente`, `Producto`, `Cita` (ejemplos) usando el mixin.
- Tests unitarios que verifican aislamiento en el Admin.
- Instrucciones para ejecutar con **MySQL** y usar **MySQL Workbench**.

---

## Estructura relevante del proyecto
```
project_root/
├─ app/                      # app principal (ej: clinic_app)
│  ├─ models.py              # Clinic, User (AbstractUser extendido), Cliente, Producto, Cita
│  ├─ managers.py            # UserManager personalizado (create_user obligatorio tenant)
│  ├─ admin.py               # Registro de ModelAdmin con TenantAdminMixin
│  ├─ admin_mixins.py        # TenantAdminMixin (reusable)
│  ├─ serializers.py         # DRF serializers (si aplica) con asignación automática de tenant
│  ├─ tests/                 # tests/test_admin_tenant.py
│  └─ migrations/
├─ requirements.txt
├─ manage.py
└─ README_Multitenancy_Admin.md
```

> Ajusta `app/` por el nombre real de tu aplicación si difiere.

---

## Requisitos
- Python 3.8+ (recomendado 3.10/3.11)
- Django 3.2 / 4.x (adaptar según tu proyecto)
- mysqlclient (recomendado) o pymysql
- MySQL Server 5.7+ o 8.x
- MySQL Workbench (opcional pero recomendado para inspección)

Instalar dependencias (ejemplo con pip):

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
# Si no tienes mysqlclient en requirements, instala:
pip install mysqlclient
# O alternativa:
pip install pymysql
```

Si usas `pymysql`, añade en `your_project/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## Configuración de la base de datos (settings.py)
Ejemplo mínimo para conectar Django a MySQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'mi_base'),
        'USER': os.environ.get('MYSQL_USER', 'mi_usuario'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'mi_pass'),
        'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

> Recomendación: usar variables de entorno (.env) y `django-environ`.

---

## Crear base de datos y usuario en MySQL (WorkBench / CLI)
Accede a MySQL y ejecuta:

```sql
CREATE DATABASE mi_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mi_usuario'@'localhost' IDENTIFIED BY 'mi_pass';
GRANT ALL PRIVILEGES ON mi_base.* TO 'mi_usuario'@'localhost';
FLUSH PRIVILEGES;
```

Si el acceso será remoto, cambia `'localhost'` por el host o `%` (menos seguro).

---

## Migraciones y preparación del esquema
Ejecuta:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Nota sobre añadir `tenant` a modelos existentes
Si agregas un campo `tenant` a modelos con datos previos, sigue estos pasos:
1. Añadir el campo `tenant` como `null=True` temporalmente.
2. `makemigrations` y `migrate`.
3. Rellenar los registros existentes con el tenant correcto (script Django o UPDATE SQL).
4. Cambiar el campo a `null=False` y migrar.

---

## Comandos útiles para crear datos iniciales
Crear superuser:

```bash
python manage.py createsuperuser
```

Crear clínicas y usuarios (ejemplo con shell):

```bash
python manage.py shell
```
```python
from app.models import Clinic, User
c1 = Clinic.objects.create(name='Clinica A')
c2 = Clinic.objects.create(name='Clinica B')
# Usuario por clinic
u1 = User.objects.create_user(username='admin_a', password='pwd', tenant=c1)
u2 = User.objects.create_user(username='admin_b', password='pwd', tenant=c2)
# Superuser ejemplo
root = User.objects.create_superuser(username='root', password='pwd', tenant=c1)
```

---

## Cómo funciona la asignación de tenant
- `User` tiene un `ForeignKey` a `Clinic` (campo `tenant`).
- El `UserManager` requiere `tenant` en `create_user` (no permite crear usuarios sin tenant).
- En vistas/APIs/serializers se fuerza la asignación de `tenant` desde `request.user.tenant` al crear usuarios nuevos (no se acepta `tenant` arbitrario en el payload).
- En el Admin, el `TenantAdminMixin`:
  - Filtra `queryset` para que muestre solo objetos cuyo `tenant` coincida con `request.user.tenant` (salvo superusers).
  - Restringe opciones de `ForeignKey` y `Inlines` a objetos del mismo tenant.
  - Evita edición o cambio de `tenant` en objetos existentes fuera del tenant del usuario.

---

## Demo rápido para el Sprint Review (pasos reproducibles)
1. Ejecutar servidor:
   ```bash
   python manage.py runserver
   ```
2. Abrir navegador e ir a `http://127.0.0.1:8000/admin/`.
3. Login como `admin_a` (tenant Clinica A).
4. Verificar en listados que solo aparecen registros de "Clinica A".
5. Intentar acceder a la URL de cambio de un objeto perteneciente a "Clinica B": `http://127.0.0.1:8000/admin/app/model/<id>/change/` — debe devolver 403 o redirigir.
6. Crear un nuevo `Cliente` desde admin — comprobar que el campo `tenant` se asigna automáticamente (si está oculto en el form) al tenant del usuario creador.
7. Iniciar sesión como `root` (superuser) y comprobar que ve todos los registros.

---

## Ejecutar tests
Se incluyen tests de aislamiento del Admin. Ejecuta:

```bash
python manage.py test
# o si usas pytest:
pytest
```

Tests de ejemplo cubren:
- Listado del admin que solo muestra registros del tenant del usuario.
- Intento de edición/visualización de objetos de otro tenant → 403/denegado.
- Creación de usuarios forzada al tenant del request.

---

## Troubleshooting (errores frecuentes)
- **Error al instalar `mysqlclient` en Windows**: instala Visual C++ Build Tools o usa `pymysql`.
- **`caching_sha2_password`**: MySQL 8 usa ese plugin; si el cliente falla, crea/ajusta el usuario con `mysql_native_password`:

```sql
ALTER USER 'mi_usuario'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mi_pass';
FLUSH PRIVILEGES;
```

- **`OperationalError: (1045, "Access denied")`**: revisar usuario/contraseña/host y permisos (`GRANT`).
- **Migración fallida por datos null**: seguir el plan de migración para agregar tenant en fases (nullable → rellenar → non-nullable).

---

## Checklist de aceptación (Entregable final)
- [ ] Tenant agregado al modelo `User` y obligatorio en creación.
- [ ] `TenantAdminMixin` aplicado a modelos relevantes (clientes, productos, citas, etc.).
- [ ] Listados, forms e inlines filtrados por tenant.
- [ ] Intentos de acceder/editar objetos de otro tenant son denegados.
- [ ] Tests automáticos pasan.
- [ ] Migraciones aplicadas y probadas en MySQL Workbench / entorno de staging.
- [ ] Documentación (este README) incluida en el repositorio.

---

## Próximos pasos recomendados
- Extender el mixin para cubrir acciones bulk y exportaciones del admin.
- Añadir logs/auditoría para cambios sensibles entre tenants.
- Evaluar performance en producción con múltiples tenants y números altos de registros.
- Considerar un enfoque de multitenancy a nivel de esquema o base de datos si el proyecto escala (hoy usamos separación por campo `tenant`).

---

## Contacto
Si necesitás que genere el archivo `README.md` para descargar o que adapte ejemplos para nombres reales de tus apps/modelos, decímelo y lo genero listo para pegar en el repo.

---

