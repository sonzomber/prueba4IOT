from django.shortcuts import render, get_object_or_404, redirect
from .models import Medico
from django.contrib.auth.decorators import login_required
from .models import Hora
from django.contrib.auth import authenticate, login
from .models import Usuario

def index(request):
    context={}
    return render(request, 'personas/index.html')


def listamedicos(request):
    medicos = Medico.objects.all()
    return render(request, 'personas/listamedicos.html', {'medicos': medicos})

def ver_horas_medico(request, medico_id):
    medico = get_object_or_404(Medico, id=medico_id)
    horas = medico.horas.filter(disponible=True).order_by('fecha', 'hora')
    return render(request, 'personas/ver_horas_medico.html', {'medico': medico, 'horas': horas})




@login_required
def reservar_hora(request, hora_id):
    hora = get_object_or_404(Hora, id=hora_id)

    if hora.disponible:  # Verificar que la hora esté disponible
        hora.disponible = False
        hora.usuario = request.user
        hora.save()  # Guardar la reserva en la base de datos
        return render(request, 'medicos/hora_reservada.html', {'hora': hora})
    else:
        return render(request, 'error.html', {'mensaje': 'La hora ya está reservada.'})
    

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
    



def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(username=username, password=password)
            # Guardar datos en la sesión
            request.session['usuario_id'] = usuario.id
            request.session['grupo'] = usuario.grupo
            if usuario.grupo == 'Paciente':
                return redirect('ver_citas_paciente')
            elif usuario.grupo == 'Medico':
                return redirect('ver_horas_medico')
        except Usuario.DoesNotExist:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'personas/login.html')



def logout_usuario(request):
    request.session.flush()  # Elimina toda la información de la sesión
    return redirect('login')



def vista_protegida(request):
    if 'usuario_id' not in request.session:
        return redirect('login')  # Redirige si no está autenticado
    # Continúa con la lógica de la vista


def registro_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        grupo = request.POST.get('grupo')

        # Verificar si el nombre de usuario ya existe
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'registro.html', {'error': 'El usuario ya existe.'})
        
        # Crear un nuevo usuario
        nuevo_usuario = Usuario.objects.create(username=username, password=password, grupo=grupo)
        nuevo_usuario.save()
        return redirect('login')  # Redirigir al formulario de inicio de sesión

    return render(request, 'personas/registro.html')