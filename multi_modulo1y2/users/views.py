from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserChangeForm

@login_required
def profile_view(request):
    """Vista para mostrar el perfil del usuario"""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    """Vista para editar el perfil del usuario"""
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('users:profile')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {'form': form})