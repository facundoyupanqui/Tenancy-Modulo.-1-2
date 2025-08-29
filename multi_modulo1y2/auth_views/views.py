from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from productos.models import Tenant
from users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    """Vista de la página principal - página de bienvenida"""
    if request.user.is_authenticated:
        # Si el usuario está autenticado, redirigir a su dashboard
        if request.user.is_superuser:
            return redirect('admin:index')
        else:
            return redirect('productos:producto_list')
    
    # Si no está autenticado, mostrar página de bienvenida
    tenants = Tenant.objects.filter(is_active=True)
    return render(request, 'login/home.html', {'tenants': tenants})

def login_view(request):
    """Vista de login con selección de tenant"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tenant_slug = request.POST.get('tenant')
        
        # Validar que se haya seleccionado un tenant
        if not tenant_slug:
            messages.error(request, 'Por favor selecciona una clínica')
            tenants = Tenant.objects.filter(is_active=True)
            return render(request, 'login/login.html', {'tenants': tenants})
        
        # Validar que se hayan proporcionado usuario y contraseña
        if not username or not password:
            messages.error(request, 'Por favor proporciona usuario y contraseña')
            tenants = Tenant.objects.filter(is_active=True)
            return render(request, 'login/login.html', {'tenants': tenants})
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar que el usuario tenga acceso al tenant seleccionado
            try:
                tenant = Tenant.objects.get(slug=tenant_slug, is_active=True)
                
                # Verificar que el usuario tenga acceso al tenant
                if user.is_superuser or (hasattr(user, 'tenant') and user.tenant == tenant):
                    # Iniciar sesión
                    login(request, user)
                    
                    # Guardar el tenant en la sesión
                    request.session['tenant_id'] = tenant.id
                    request.session['tenant_name'] = tenant.name
                    
                    messages.success(request, f'Bienvenido a {tenant.name}')
                    
                    # Redirigir según el rol del usuario
                    if user.is_superuser:
                        return redirect('admin:index')
                    else:
                        return redirect('productos:producto_list')
                else:
                    messages.error(request, f'No tienes acceso a la clínica {tenant.name}')
            except Tenant.DoesNotExist:
                messages.error(request, 'La clínica seleccionada no existe o no está activa')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    # Obtener todas las clínicas activas para mostrar en el formulario
    tenants = Tenant.objects.filter(is_active=True)
    return render(request, 'login/login.html', {'tenants': tenants})

def logout_view(request):
    """Vista para cerrar sesión"""
    # Limpiar la información del tenant de la sesión
    if 'tenant_id' in request.session:
        del request.session['tenant_id']
    if 'tenant_name' in request.session:
        del request.session['tenant_name']
        
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('home')

def error_no_tenant(request):
    """Vista para mostrar error cuando un usuario no tiene tenant asignado"""
    return render(request, 'login/error_no_tenant.html')

def register_view(request):
    """Vista de registro con selección de tenant"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # El tenant ya está asignado por el formulario
            user.save()
            
            # Iniciar sesión automáticamente después del registro
            login(request, user)
            
            # Guardar el tenant en la sesión
            request.session['tenant_id'] = user.tenant.id
            request.session['tenant_name'] = user.tenant.name
            
            messages.success(request, f'Cuenta creada exitosamente. Bienvenido a {user.tenant.name}')
            return redirect('productos:producto_list')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    # Pasar el formulario y los tenants a la plantilla
    tenants = Tenant.objects.filter(is_active=True)
    return render(request, 'login/register.html', {'form': form, 'tenants': tenants})