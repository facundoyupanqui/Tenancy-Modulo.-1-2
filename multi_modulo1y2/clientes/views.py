from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente
from .forms import ClienteForm

@login_required
def cliente_list(request):
    # Filtrar clientes por el tenant del usuario autenticado
    clientes = Cliente.objects.filter(tenant=request.user.tenant)
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})

@login_required
def cliente_detail(request, pk):
    # Asegurar que el cliente pertenece al tenant del usuario
    cliente = get_object_or_404(Cliente, pk=pk, tenant=request.user.tenant)
    return render(request, 'clientes/cliente_detail.html', {'cliente': cliente})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.tenant = request.user.tenant  # Asignar automáticamente el tenant del usuario
            cliente.save()
            return redirect('clientes:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm()
    return render(request, 'clientes/cliente_form.html', {'form': form})

@login_required
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, tenant=request.user.tenant)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:cliente_detail', pk=cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'clientes/cliente_form.html', {'form': form})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk, tenant=request.user.tenant)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes:cliente_list')
    return render(request, 'clientes/cliente_confirm_delete.html', {'cliente': cliente})