from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Producto, Tenant

def lista_productos(request):
    """Vista para listar productos del tenant del usuario"""
    # Vista simplificada para evitar errores
    context = {
        'productos': [],
        'tenant': None
    }
    return render(request, 'productos/lista_productos.html', context)

@login_required
def detalle_producto(request, pk):
    """Vista para mostrar detalles de un producto"""
    try:
        tenant = request.user.usuariotenant.tenant
        producto = get_object_or_404(Producto, pk=pk, tenant=tenant)
        
        context = {
            'producto': producto,
            'tenant': tenant
        }
        return render(request, 'productos/detalle_producto.html', context)
    except:
        messages.error(request, 'Producto no encontrado o sin acceso')
        return redirect('lista_productos')

@login_required
def crear_producto(request):
    """Vista para crear un nuevo producto"""
    if request.method == 'POST':
        # Aquí implementaremos la lógica para crear productos
        pass
    
    try:
        tenant = request.user.usuariotenant.tenant
        context = {
            'tenant': tenant
        }
        return render(request, 'productos/crear_producto.html', context)
    except:
        messages.error(request, 'No tienes permisos para crear productos')
        return redirect('lista_productos') 