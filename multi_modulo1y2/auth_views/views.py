from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from productos.models import Tenant
from clientes.models import UsuarioTenant

def home(request):
    """Vista de la página principal - redirige al login"""
    return redirect('auth_views:login')

def login_view(request):
    """Vista de login con selección de tenant"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        tenant_slug = request.POST.get('tenant')
        
        # Validar que se haya seleccionado un tenant
        if not tenant_slug:
            messages.error(request, 'Por favor selecciona una clínica')
            return render(request, 'login/login.html')
        
        # Autenticar usuario
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Verificar que el usuario tenga acceso al tenant seleccionado
            try:
                tenant = Tenant.objects.get(slug=tenant_slug, is_active=True)
                usuario_tenant = UsuarioTenant.objects.get(user=user, tenant=tenant, is_active=True)
                
                # Iniciar sesión
                login(request, user)
                
                # Guardar el tenant en la sesión
                request.session['tenant_id'] = tenant.id
                request.session['tenant_name'] = tenant.name
                
                messages.success(request, f'Bienvenido a {tenant.name}')
                return redirect('productos:lista_productos')
                
            except (Tenant.DoesNotExist, UsuarioTenant.DoesNotExist):
                messages.error(request, 'No tienes acceso a esta clínica')
                return render(request, 'login/login.html')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login/login.html')

@login_required
def logout_view(request):
    """Vista de logout"""
    # Limpiar la sesión del tenant
    if 'tenant_id' in request.session:
        del request.session['tenant_id']
    if 'tenant_name' in request.session:
        del request.session['tenant_name']
    
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente')
    return redirect('auth_views:login')

def dashboard(request):
    """Vista del dashboard principal"""
    if not request.user.is_authenticated:
        return redirect('auth_views:login')
    
    try:
        tenant = request.user.usuariotenant.tenant
        context = {
            'tenant': tenant,
            'user': request.user
        }
        return render(request, 'dashboard.html', context)
    except:
        messages.error(request, 'No se pudo cargar el dashboard')
        return redirect('auth_views:login') 