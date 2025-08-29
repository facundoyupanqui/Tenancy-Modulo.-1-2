from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import date, timedelta, datetime
from .models import Cita, Doctor, Especialidad
from .forms import CitaForm, CitaSearchForm

@login_required
def cita_list(request):
    """Vista para listar las citas del usuario"""
    # Obtener citas del usuario
    citas = Cita.objects.filter(
        paciente=request.user,
        tenant=request.user.tenant
    ).select_related('doctor', 'doctor__especialidad').order_by('-fecha', '-hora')
    
    # Formulario de búsqueda
    search_form = CitaSearchForm(request.GET, user=request.user)
    
    if search_form.is_valid():
        fecha_desde = search_form.cleaned_data.get('fecha_desde')
        fecha_hasta = search_form.cleaned_data.get('fecha_hasta')
        doctor = search_form.cleaned_data.get('doctor')
        estado = search_form.cleaned_data.get('estado')
        
        if fecha_desde:
            citas = citas.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            citas = citas.filter(fecha__lte=fecha_hasta)
        if doctor:
            citas = citas.filter(doctor=doctor)
        if estado:
            citas = citas.filter(estado=estado)
    
    # Agrupar citas por fecha
    citas_por_fecha = {}
    for cita in citas:
        fecha_str = cita.fecha.strftime('%Y-%m-%d')
        if fecha_str not in citas_por_fecha:
            citas_por_fecha[fecha_str] = []
        citas_por_fecha[fecha_str].append(cita)
    
    context = {
        'citas': citas,
        'citas_por_fecha': citas_por_fecha,
        'search_form': search_form,
        'estados': Cita.ESTADO_CHOICES,
    }
    
    return render(request, 'citas_medicas/cita_list.html', context)

@login_required
def cita_detail(request, pk):
    """Vista para mostrar el detalle de una cita"""
    cita = get_object_or_404(
        Cita, 
        pk=pk, 
        paciente=request.user,
        tenant=request.user.tenant
    )
    
    return render(request, 'citas_medicas/cita_detail.html', {'cita': cita})

@login_required
def cita_create(request):
    """Vista para crear una nueva cita"""
    if request.method == 'POST':
        form = CitaForm(request.POST, user=request.user)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.paciente = request.user
            cita.tenant = request.user.tenant
            cita.save()
            
            messages.success(
                request, 
                f'Cita programada exitosamente para el {cita.fecha} a las {cita.hora}'
            )
            return redirect('citas_medicas:cita_detail', pk=cita.pk)
    else:
        form = CitaForm(user=request.user)
    
    # Obtener doctores disponibles
    doctores = Doctor.objects.filter(
        tenant=request.user.tenant,
        is_active=True
    ).select_related('especialidad')
    
    context = {
        'form': form,
        'doctores': doctores,
    }
    
    return render(request, 'citas_medicas/cita_form.html', context)

@login_required
def cita_update(request, pk):
    """Vista para editar una cita"""
    cita = get_object_or_404(
        Cita, 
        pk=pk, 
        paciente=request.user,
        tenant=request.user.tenant
    )
    
    # Solo permitir editar citas programadas o confirmadas
    if cita.estado not in ['programada', 'confirmada']:
        messages.error(request, 'No se puede editar una cita que ya fue atendida o cancelada.')
        return redirect('citas_medicas:cita_detail', pk=cita.pk)
    
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('citas_medicas:cita_detail', pk=cita.pk)
    else:
        form = CitaForm(instance=cita, user=request.user)
    
    context = {
        'form': form,
        'cita': cita,
    }
    
    return render(request, 'citas_medicas/cita_form.html', context)

@login_required
def cita_cancel(request, pk):
    """Vista para cancelar una cita"""
    cita = get_object_or_404(
        Cita, 
        pk=pk, 
        paciente=request.user,
        tenant=request.user.tenant
    )
    
    # Solo permitir cancelar citas programadas o confirmadas
    if cita.estado not in ['programada', 'confirmada']:
        messages.error(request, 'No se puede cancelar una cita que ya fue atendida o cancelada.')
        return redirect('citas_medicas:cita_detail', pk=cita.pk)
    
    if request.method == 'POST':
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'Cita cancelada exitosamente.')
        return redirect('citas_medicas:cita_list')
    
    return render(request, 'citas_medicas/cita_confirm_cancel.html', {'cita': cita})

@login_required
def doctor_list(request):
    """Vista para listar los doctores disponibles"""
    doctores = Doctor.objects.filter(
        tenant=request.user.tenant,
        is_active=True
    ).select_related('especialidad')
    
    # Agrupar por especialidad
    doctores_por_especialidad = {}
    for doctor in doctores:
        especialidad = doctor.especialidad.nombre
        if especialidad not in doctores_por_especialidad:
            doctores_por_especialidad[especialidad] = []
        doctores_por_especialidad[especialidad].append(doctor)
    
    context = {
        'doctores': doctores,
        'doctores_por_especialidad': doctores_por_especialidad,
    }
    
    return render(request, 'citas_medicas/doctor_list.html', context)

@login_required
def doctor_detail(request, pk):
    """Vista para mostrar el detalle de un doctor"""
    doctor = get_object_or_404(
        Doctor, 
        pk=pk, 
        tenant=request.user.tenant,
        is_active=True
    )
    
    # Obtener próximas citas disponibles
    proximas_citas = []
    today = date.today()
    
    for i in range(7):  # Próximos 7 días
        fecha = today + timedelta(days=i)
        if fecha.weekday() < 5:  # Solo días laborables (lunes a viernes)
            # Generar horarios disponibles
            hora_actual = doctor.horario_inicio
            while hora_actual <= doctor.horario_fin:
                # Verificar si hay cita en este horario
                if not Cita.objects.filter(
                    doctor=doctor,
                    fecha=fecha,
                    hora=hora_actual,
                    estado__in=['programada', 'confirmada']
                ).exists():
                    proximas_citas.append({
                        'fecha': fecha,
                        'hora': hora_actual,
                        'disponible': True
                    })
                
                # Incrementar hora (30 minutos)
                hora_actual = (datetime.combine(date.min, hora_actual) + timedelta(minutes=30)).time()
    
    context = {
        'doctor': doctor,
        'proximas_citas': proximas_citas[:20],  # Limitar a 20 opciones
    }
    
    return render(request, 'citas_medicas/doctor_detail.html', context)
