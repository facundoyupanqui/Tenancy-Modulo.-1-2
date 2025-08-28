# 📚 DOCUMENTACIÓN COMPLETA - SISTEMA MULTITENANCY
## LOGIN Y ADMIN

---

## 🚀 **1. EJECUTAR EL SERVIDOR**

### **Opción A: Desde PowerShell/CMD**
```bash
# Navegar al directorio del proyecto
cd "C:\Users\Christian\Desktop\xammp\htdocs\TENANCY_MODULO01\Tenancy-Modulo.-1-2\multi_modulo1y2"

# Activar el entorno virtual (si lo tienes)
 .\venv\Scripts\activate

# Ejecutar el servidor
python manage.py runserver
```

### **Opción B: Desde VS Code/Cursor**
1. Abrir la terminal integrada
2. Navegar al directorio del proyecto
3. Ejecutar: `python manage.py runserver`

### **Resultado Esperado:**
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
August 28, 2025 - 04:XX:XX
Django version 5.2.5, using settings 'multi_tenant_modulo1y2.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 🔐 **2. ACCESO AL ADMIN DE DJANGO**

### **URL del Admin:**
```
http://127.0.0.1:8000/admin/
```

### **Credenciales (usar las que creaste antes):**
- **Usuario:** [Tu nombre de usuario]
- **Contraseña:** [Tu contraseña]

### **Pasos en el Admin:**

#### **2.1 Crear Tenants (Clínicas)**
1. Ir a **Admin > Tenants**
2. Hacer clic en **"Add Tenant"**
3. Llenar los campos:
   - **Name:** `Clínica A`
   - **Slug:** `clinica_a`
   - **Is Active:** ✅ (marcado)
4. Hacer clic en **"Save"**
5. Repetir para **Clínica B**:
   - **Name:** `Clínica B`
   - **Slug:** `clinica_b`

#### **2.2 Crear Usuarios del Sistema**
1. Ir a **Admin > Users**
2. Hacer clic en **"Add User"**
3. Crear usuario para Clínica A:
   - **Username:** `admin_clinica_a`
   - **Email:** `admin@clinicaa.com`
   - **Password:** [contraseña segura]
   - **Is Staff:** ✅ (marcado)
   - **Is Superuser:** ❌ (desmarcado)
4. Hacer clic en **"Save and add another"**

#### **2.3 Vincular Usuarios con Tenants**
1. Ir a **Admin > Usuario Tenants**
2. Hacer clic en **"Add Usuario Tenant"**
3. Llenar los campos:
   - **User:** `admin_clinica_a`
   - **Tenant:** `Clínica A`
   - **Rol:** `admin`
   - **Is Active:** ✅ (marcado)
4. Hacer clic en **"Save"**

---

## 🎯 **3. ACCESO AL LOGIN DEL SISTEMA**

### **URL del Login:**
```
http://127.0.0.1:8000/
```
**O directamente:**
```
http://127.0.0.1:8000/login/
```

### **Pasos para el Login:**

#### **3.1 Seleccionar Clínica**
- En el dropdown **"Clínica"** seleccionar:
  - `Clínica A` o
  - `Clínica B`

#### **3.2 Ingresar Credenciales**
- **Usuario:** `admin_clinica_a`
- **Contraseña:** [la que creaste]

#### **3.3 Acceder al Sistema**
- Hacer clic en **"Iniciar Sesión"**
- Deberías ser redirigido al dashboard

---

## 📊 **4. VERIFICAR EL AISLAMIENTO POR TENANT**

### **4.1 Crear Datos de Prueba**

#### **Crear Productos:**
1. Ir a **Admin > Productos**
2. Crear producto para Clínica A:
   - **Tenant:** `Clínica A`
   - **Nombre:** `Medicamento A`
   - **Precio:** `25.50`
   - **Stock:** `100`
   - **Categoría:** `Medicamentos`

#### **Crear Clientes:**
1. Ir a **Admin > Clientes**
2. Crear cliente para Clínica A:
   - **Tenant:** `Clínica A`
   - **Nombre:** `Juan Pérez`
   - **Apellido:** `García`
   - **Email:** `juan@email.com`

### **4.2 Probar Aislamiento:**
1. **Cerrar sesión** del admin
2. **Iniciar sesión** con usuario de Clínica A
3. **Verificar** que solo vea datos de Clínica A
4. **Confirmar** que no pueda ver datos de Clínica B

---

## 🛠️ **5. COMANDOS ÚTILES DEL TERMINAL**

### **5.1 Gestión del Proyecto**
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

# Ejecutar servidor en puerto específico
python manage.py runserver 8080

# Ejecutar servidor accesible desde red
python manage.py runserver 0.0.0.0:8000
```

### **5.2 Verificar Estado**
```bash
# Verificar configuración
python manage.py check

# Verificar URLs
python manage.py show_urls

# Shell de Django
python manage.py shell
```

---

## 🔍 **6. SOLUCIÓN DE PROBLEMAS COMUNES**

### **6.1 Error "NoReverseMatch"**
- **Causa:** URLs mal configuradas
- **Solución:** Verificar `urls.py` y nombres de URLs

### **6.2 Error de Base de Datos**
- **Causa:** Migraciones no aplicadas
- **Solución:** Ejecutar `python manage.py migrate`

### **6.3 Error de Módulo pymysql**
- **Causa:** Dependencia no instalada
- **Solución:** `pip install pymysql`

### **6.4 Error de Templates**
- **Causa:** Carpeta templates no encontrada
- **Solución:** Verificar ruta en `settings.py`

---

## 🌐 **7. ESTRUCTURA DE URLs DEL SISTEMA**

```
http://127.0.0.1:8000/           → Login (página principal)
http://127.0.0.1:8000/login/     → Login directo
http://127.0.0.1:8000/admin/     → Admin de Django
http://127.0.0.1:8000/productos/ → Lista de productos
http://127.0.0.1:8000/clientes/  → Lista de clientes
http://127.0.0.1:8000/logout/    → Cerrar sesión
```

---

## 🎯 **8. FLUJO COMPLETO DE PRUEBA**

### **Paso 1: Preparación**
1. Ejecutar servidor: `python manage.py runserver`
2. Abrir navegador: `http://127.0.0.1:8000/admin/`

### **Paso 2: Configuración Inicial**
1. Crear tenants (Clínica A, Clínica B)
2. Crear usuarios para cada clínica
3. Vincular usuarios con tenants

### **Paso 3: Prueba del Sistema**
1. Ir a: `http://127.0.0.1:8000/`
2. Seleccionar clínica
3. Iniciar sesión
4. Verificar acceso solo a datos de la clínica

### **Paso 4: Verificación de Aislamiento**
1. Crear datos en ambas clínicas
2. Cambiar entre usuarios de diferentes clínicas
3. Confirmar que no hay acceso cruzado

---

## 📞 **9. SOPORTE TÉCNICO**

### **Si algo no funciona:**
1. **Revisar consola** del servidor para errores
2. **Verificar logs** de Django
3. **Comprobar configuración** de base de datos
4. **Revisar migraciones** aplicadas

### **Comandos de diagnóstico:**
```bash
# Verificar estado del proyecto
python manage.py check --deploy

# Verificar conexión a base de datos
python manage.py dbshell

# Verificar templates
python manage.py collectstatic --dry-run
```

---

## 🔧 **10. CONFIGURACIÓN DE BASE DE DATOS**

### **Verificar conexión MySQL:**
- **Host:** 127.0.0.1
- **Puerto:** 3306
- **Base de datos:** modulo1y2
- **Usuario:** root
- **Contraseña:** [Tu contraseña de MySQL]

### **Si hay problemas de conexión:**
1. Verificar que XAMPP esté ejecutándose
2. Verificar que MySQL esté activo
3. Verificar credenciales en `settings.py`

---

## 📋 **11. CHECKLIST DE VERIFICACIÓN**

### **Antes de empezar:**
- [ ] XAMPP ejecutándose
- [ ] MySQL activo
- [ ] Base de datos `modulo1y2` creada
- [ ] Dependencias instaladas (`pip install pymysql`)

### **Después de la configuración:**
- [ ] Servidor ejecutándose sin errores
- [ ] Admin accesible en `/admin/`
- [ ] Login accesible en `/`
- [ ] Tenants creados en el admin
- [ ] Usuarios vinculados a tenants
- [ ] Aislamiento funcionando correctamente

---

## 🎉 **12. ¡LISTO PARA USAR!**

Una vez completados todos los pasos, tendrás un sistema multitenancy completamente funcional donde:

✅ **Cada clínica tiene acceso independiente a sus datos**
✅ **Los usuarios solo ven información de su tenant**
✅ **El admin filtra automáticamente por tenant**
✅ **El login redirige correctamente al sistema**

---

**📧 Para soporte técnico o dudas:**
- Revisar esta documentación
- Verificar logs del servidor
- Comprobar configuración paso a paso

**🚀 ¡Disfruta tu sistema multitenancy!** 