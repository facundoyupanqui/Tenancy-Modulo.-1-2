from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto
from .forms import ProductoForm

@login_required
def producto_list(request):
    # Filtrar productos por el tenant del usuario autenticado
    productos = Producto.objects.filter(tenant=request.user.tenant)
    return render(request, 'productos/producto_list.html', {'productos': productos})

@login_required
def producto_detail(request, pk):
    # Asegurar que el producto pertenece al tenant del usuario
    producto = get_object_or_404(Producto, pk=pk, tenant=request.user.tenant)
    return render(request, 'productos/producto_detail.html', {'producto': producto})

@login_required
def producto_create(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.tenant = request.user.tenant  # Asignar automáticamente el tenant del usuario
            producto.save()
            return redirect('productos:producto_detail', pk=producto.pk)
    else:
        form = ProductoForm()
    return render(request, 'productos/producto_form.html', {'form': form})

@login_required
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk, tenant=request.user.tenant)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos:producto_detail', pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'productos/producto_form.html', {'form': form})

@login_required
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk, tenant=request.user.tenant)
    if request.method == 'POST':
        producto.delete()
        return redirect('productos:producto_list')
    return render(request, 'productos/producto_confirm_delete.html', {'producto': producto})