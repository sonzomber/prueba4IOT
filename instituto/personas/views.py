from django.shortcuts import render, get_object_or_404, redirect
from .models import Medico
from django.contrib.auth.decorators import login_required
from .models import Hora
from .models import Usuario

def index(request):
    context={}
    return render(request, 'personas/index.html')


def listamedicos(request):
    medicos = Medico.objects.all()
    return render(request, 'personas/listamedicos.html', {'medicos': medicos})

def ver_horas_medico(request, medico_id):
    # Obtener el médico correspondiente al ID
    medico = get_object_or_404(Medico, id=medico_id)

    # Filtrar las horas disponibles para este médico
    horas = medico.horas.filter(disponible=True).order_by('fecha', 'hora')

    return render(request, 'personas/ver_horas_medico.html', {'medico': medico, 'horas': horas})




def reservar_hora(request, hora_id):
    # Obtener la hora específica
    hora = get_object_or_404(Hora, id=hora_id)

    if hora.disponible:  # Verificar disponibilidad
        # Marcar como reservada
        hora.disponible = False
        hora.usuario = request.user  # Asigna el paciente actual
        hora.save()

        # Redirigir a una página de confirmación
        return render(request, 'personas/hora_reservada.html', {'hora': hora})
    

def ver_citas_paciente(request):
    if not request.session.get('usuario_id'):
        return render(request, 'error.html', {'mensaje': 'Debes iniciar sesión para acceder a esta página.'})
    if request.session.get('grupo') != "Paciente":
        return render(request, 'error.html', {'mensaje': 'No tienes permisos para acceder a esta página.'})
    # Resto de la lógica para mostrar las citas

@login_required
def ver_horas_pacientes_medico(request):
    # Verificar si el usuario pertenece al grupo "Médicos"
    if request.user.groups.filter(name="Médicos").exists():
        # Filtrar las horas asociadas al médico actual
        horas = Hora.objects.filter(medico__nombre=request.user.username).order_by('fecha', 'hora')
        return render(request, 'medicos/ver_horas_pacientes.html', {'horas': horas})
    else:
        # Si no pertenece al grupo "Médicos", mostrar un mensaje de error
        return render(request, 'error.html', {'mensaje': 'No tienes permisos para acceder a esta página.'})
    



def login_medico(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            medico = Medico.objects.get(nombre=username)
            if medico.check_password(password):  # Verificar contraseña
                request.session['medico_id'] = medico.id
                return redirect('gestionar_horas')
            else:
                return render(request, 'personas/login.html', {'error': 'Contraseña incorrecta'})
        except Medico.DoesNotExist:
            return render(request, 'personas/login.html', {'error': 'Médico no encontrado'})
    return render(request, 'personas/login.html')


def logout_usuario(request):
    request.session.flush()  # Elimina toda la información de la sesión
    return redirect('login')



def vista_protegida(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redirige si no está autenticado
    # Continúa con la lógica de la vista







def gestionar_horas(request):
    medico_id = request.session.get('medico_id')  # Obtener ID del médico autenticado
    if not medico_id:
        return redirect('login_medico')

    medico = get_object_or_404(Medico, id=medico_id)
    horas = medico.horas.order_by('fecha', 'hora')  # Todas las horas asociadas al médico

    return render(request, 'personas/gestionar_horas.html', {'medico': medico, 'horas': horas})


def gestionar_horas_accion(request, hora_id):
    hora = get_object_or_404(Hora, id=hora_id)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        if accion == 'realizada':
            hora.disponible = False  # Marcamos como no disponible (realizada)
            hora.usuario = None  # Limpia el usuario si lo prefieres
        elif accion == 'cancelar':
            hora.disponible = True  # La hora vuelve a estar disponible
            hora.usuario = None
        hora.save()
        return redirect('gestionar_horas')

    return redirect('gestionar_horas')