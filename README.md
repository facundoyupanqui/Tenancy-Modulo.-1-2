# Tenancy Módulo 1 y 2

Proyecto Django multi-tenant con base de datos MySQL.

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

### 4. Configurar la base de datos MySQL

- Crea la base de datos en MySQL:
  ```sql
  CREATE DATABASE modulo1y2 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
  ```
- Asegúrate de que el usuario y contraseña en `multi_tenant_modulo1y2/settings.py` sean correctos.

### 5. Aplicar migraciones
```sh
python manage.py makemigrations
python manage.py migrate
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
└───multi_tenant_modulo1y2/
    │   __init__.py
    │   asgi.py
    │   settings.py
    │   urls.py
    │   wsgi.py
```

---

## 📝 Notas

- Revisa y ajusta los datos de conexión a MySQL en `settings.py`.
- Si usas PyMySQL, asegúrate de agregar:
  ```python
  import pymysql
  pymysql.install_as_MySQLdb()
  ```
  al inicio de tu `settings.py`.

---

## 📚 Documentación

- [Documentación oficial de Django](https://docs.djangoproject.com/en/5.2/)
- [Documentación oficial de MySQL](https://dev.mysql.com/doc/)

---

## 🛠️ Requerimientos

Ver archivo `requirements.txt`.

---

## Licencia

Este proyecto está bajo la licencia MIT.