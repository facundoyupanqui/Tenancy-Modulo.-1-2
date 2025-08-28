# Tenancy Módulo 1 y 2

> **Proyecto:** Sistema Django multitenant para gestión de clínicas (Módulos 1 y 2)
>
>
>
> Este proyecto contiene el scaffold y las implementaciones iniciales para un sistema **multitenant** pensado para clínicas. Está diseñado para que cada *tenant* represente una clínica y para que todos los recursos (usuarios, pacientes, citas, productos, etc.) queden **aislados por tenant**.
>
> El foco del Módulo 2 — Autenticaciones — es garantizar que **cada usuario pertenezca a una clínica (tenant)**, que esa relación sea obligatoria al crear usuarios y que **no pueda modificarse manualmente** por usuarios normales.

---

# 📌 Objetivos del proyecto

* Implementar multitenancy básico a nivel de aplicación (campo `tenant` en modelos).
* Extender el modelo `User` para que guarde la relación con `Clinic`.
* Asegurar la asignación automática del tenant al crear usuarios (Admin / API).
* Evitar la re-asignación manual del `tenant` una vez creado el usuario.
* Proteger el Django Admin y las vistas para que respeten el aislamiento por tenant.

---

# 🧭 Alcance del README

Esta documentación incluye:

* Presentación técnica y decisiones de diseño.
* Requisitos y tecnología usada.
* Guía paso a paso de instalación y ejecución (local y Docker).
* Ejemplos de configuración de MySQL (Workbench y SQL CLI).
* Descripción detallada de los cambios clave (modelos, managers, admin mixin).
* Plan de migración si ya existen usuarios en la base de datos.
* Tests, debugging y troubleshooting.
* Checklist de aceptación para el Módulo 2.

---

# 🧰 Stack tecnológico

* Python 3.10+
* Django 4.x / 5.x (según `requirements.txt` del repo)
* MySQL 8.x (o 5.7+)
* `mysqlclient` o `PyMySQL` (fallback)
* Opcional: Django REST Framework (si hay APIs)

---

# 📁 Estructura del proyecto (resumen)

```text
multi_modulo1y2/
│   manage.py
│   requirements.txt
│   README.md  # este documento
└───multi_tenant_modulo1y2/
    │   settings.py
    │   urls.py
    │   wsgi.py
└───clinic_app/   # implementación del Módulo 2
    │   models.py
    │   managers.py
    │   admin.py
    │   admin_mixins.py
    │   tests/
```

---

# 🚀 Instalación y configuración (detallado)

## 1) Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Tenancy-Modulo.-1-2/multi_modulo1y2
```

## 2) Entorno virtual y dependencias

Crear y activar venv (recomendado):

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Si `mysqlclient` da problemas en Windows, instala `pymysql` como alternativa y añade `import pymysql; pymysql.install_as_MySQLdb()` en `multi_tenant_modulo1y2/__init__.py`.

## 3) Variables de entorno (.env)

Crea un archivo `.env` en la raíz con las credenciales (no subir al repo):

```
SECRET_KEY=tu_secret_key
DEBUG=True
MYSQL_DATABASE=modulo1y2
MYSQL_USER=mi_usuario
MYSQL_PASSWORD=mi_pass
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

En `settings.py` usa `os.environ.get(...)` para leerlas.

## 4) Crear base de datos en MySQL (CLI o Workbench)

**SQL mínimo:**

```sql
CREATE DATABASE modulo1y2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mi_usuario'@'localhost' IDENTIFIED BY 'mi_pass';
GRANT ALL PRIVILEGES ON modulo1y2.* TO 'mi_usuario'@'localhost';
FLUSH PRIVILEGES;
```

En MySQL Workbench: conecta, abre SQL Editor y ejecuta las mismas sentencias.

## 5) Configurar `settings.py` (fragmento)

```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': os.environ.get('MYSQL_DATABASE'),
    'USER': os.environ.get('MYSQL_USER'),
    'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
    'HOST': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'PORT': os.environ.get('MYSQL_PORT', '3306'),
    'OPTIONS': {'charset': 'utf8mb4', 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"},
  }
}

AUTH_USER_MODEL = 'clinic_app.User'
```

## 6) Migraciones y superuser

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 7) Ejecutar servidor de desarrollo

```bash
python manage.py runserver
# abrir http://127.0.0.1:8000/admin
```

---

# 🧩 Diseño técnico (cómo funciona internamente)

## Modelo `Clinic` (tenant)

* Representa una clínica y es la entidad a la que pertenecen recursos.
* Campos mínimos: `id`, `name` (único), meta (timestamps opcional).

## Usuario extendido (`User`)

* Hereda de `AbstractUser` y añade `tenant = ForeignKey(Clinic, on_delete=PROTECT)`.
* `UserManager` personalizado que obliga pasar `tenant` en `create_user` (salvo superuser si se decide permitirlo).
* `save()` del modelo valida que si `self.pk` existe, el `tenant` no haya cambiado; en ese caso lanza `ValidationError`.

**Ejemplo (simplificado):**

```python
class User(AbstractUser):
    tenant = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name='users')

    def save(self, *args, **kwargs):
        if self.pk:
            orig = User.objects.get(pk=self.pk)
            if orig.tenant_id != self.tenant_id:
                raise ValidationError('No puede cambiar el tenant del usuario.')
        super().save(*args, **kwargs)
```

## Asignación automática del tenant

* En **Django Admin**: `UserAdmin.save_model` asigna `obj.tenant = request.user.tenant` si quien crea no es superuser.
* En **API / Serializers**: `create()` del serializer fuerza `validated_data['tenant'] = request.user.tenant`.
* En **scripts** o tareas administrativas autorizadas, se puede pasar `tenant` explícitamente.

## Protecciones en Admin

* `TenantAdminMixin` aplicado a los `ModelAdmin`:

  * `get_queryset` filtra por `request.user.tenant` (excepto superuser).
  * `formfield_for_foreignkey` limita FK a objetos del tenant.
  * `save_model` evita creación con tenant diferente y evita cambiar tenant.
  * `has_change_permission/has_view_permission` controlan acceso por objeto.

---

# 🔁 Plan de migración (si ya existen usuarios sin tenant)

1. **Agregar campo tenant como nullable**:

   * `tenant = ForeignKey(Clinic, on_delete=PROTECT, null=True, blank=True)`
   * `makemigrations` + `migrate`
2. **Rellenar datos**:

   * Escribir script Django o SQL para asignar `tenant_id` a usuarios existentes según la lógica del negocio.
   * Ejemplo rápido (Django shell):

     ```python
     from clinic_app.models import User, Clinic
     default_clinic = Clinic.objects.get(name='Clinica Default')
     User.objects.filter(tenant__isnull=True).update(tenant=default_clinic)
     ```
3. **Forzar non-null y restricciones**:

   * Cambiar campo a `null=False`, `blank=False`, `on_delete=PROTECT`.
   * `makemigrations` + `migrate`
4. **Revisar integridad** y ejecutar tests.

---

# 🧪 Tests y validación

Ejecutar tests:

```bash
python manage.py test
# o con pytest:
pytest
```

Pruebas recomendadas:

* Creación de `Clinic` y `User` con tenant asignado.
* Comprobación de que un user no ve objetos de otro tenant en Admin.
* Intento de cambiar tenant en un usuario existente -> debe fallar.

Ejemplo de caso de prueba (resumido):

```python
def test_user_tenant_assignment(client):
    # crear clinics y users, loguear admin y crear user nuevo -> comprobar tenant
    pass
```

---

# 🐳 Uso con Docker (opcional) — docker-compose mínimo

```yaml
version: '3.8'
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpass
      MYSQL_DATABASE: modulo1y2
      MYSQL_USER: mi_usuario
      MYSQL_PASSWORD: mi_pass
    ports:
      - '3306:3306'
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

  web:
    build: .
    command: bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - .:/code
    ports:
      - '8000:8000'
    depends_on:
      - db
    environment:
      - MYSQL_DATABASE=modulo1y2
      - MYSQL_USER=mi_usuario
      - MYSQL_PASSWORD=mi_pass
      - MYSQL_HOST=db
```

> Recuerda no usar estas contraseñas en producción.

---

# 🛠️ Debugging y soluciones a problemas comunes

| Problema                             | Causa posible                       | Solución rápida                                                                           |
| ------------------------------------ | ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `mysqlclient` no instala en Windows  | Falta Visual C++ Build Tools        | Instalar Build Tools o usar `pymysql`                                                     |
| `caching_sha2_password` error        | Driver antiguo no soporta plugin    | `ALTER USER 'mi_usuario'@'localhost' IDENTIFIED WITH mysql_native_password BY 'mi_pass';` |
| `OperationalError: Access denied`    | Credenciales incorrectas o host     | Revisar usuario/host/GRANTs en MySQL                                                      |
| Migración fallida por null en tenant | Campo non-null con datos existentes | Seguir plan de migración (nullable → rellenar → non-null)                                 |

---

# ✅ Checklist de aceptación (Módulo 2 – Autenticaciones)

*

---

# 📚 Referencias y lecturas recomendadas

* Django authentication: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)
* MySQL docs: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* Artículo sobre patterns multitenancy: Martin Fowler, multitenancy patterns

---

---
