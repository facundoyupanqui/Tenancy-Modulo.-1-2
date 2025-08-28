from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cliente, UsuarioTenant
from productos.models import Tenant

@login_required
def lista_clientes(request):
    """Vista para listar clientes del tenant del usuario"""
    try:
        # Obtener el tenant del usuario
        tenant = request.user.usuariotenant.tenant
        clientes = Cliente.objects.filter(tenant=tenant, is_active=True)
        
        context = {
            'clientes': clientes,
            'tenant': tenant
        }
        return render(request, 'clientes/lista_clientes.html', context)
    except:
        messages.error(request, 'No tienes acceso a clientes')
        return redirect('login')

@login_required
def detalle_cliente(request, pk):
    """Vista para mostrar detalles de un cliente"""
    try:
        tenant = request.user.usuariotenant.tenant
        cliente = get_object_or_404(Cliente, pk=pk, tenant=tenant)
        
        context = {
            'cliente': cliente,
            'tenant': tenant
        }
        return render(request, 'clientes/detalle_cliente.html', context)
    except:
        messages.error(request, 'Cliente no encontrado o sin acceso')
        return redirect('lista_clientes')

@login_required
def crear_cliente(request):
    """Vista para crear un nuevo cliente"""
    if request.method == 'POST':
        # Aquí implementaremos la lógica para crear clientes
        pass
    
    try:
        tenant = request.user.usuariotenant.tenant
        context = {
            'tenant': tenant
        }
        return render(request, 'clientes/crear_cliente.html', context)
    except:
        messages.error(request, 'No tienes permisos para crear clientes')
        return redirect('lista_clientes')

@login_required
def perfil_usuario(request):
    """Vista para mostrar el perfil del usuario actual"""
    try:
        tenant = request.user.usuariotenant.tenant
        usuario_tenant = request.user.usuariotenant
        
        context = {
            'usuario_tenant': usuario_tenant,
            'tenant': tenant
        }
        return render(request, 'clientes/perfil_usuario.html', context)
    except:
        messages.error(request, 'No se pudo cargar tu perfil')
        return redirect('login') 