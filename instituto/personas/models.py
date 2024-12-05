from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.hashers import make_password, check_password

class Medico(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    foto = models.ImageField(upload_to='medicos_fotos/', null=True, blank=True)
    contraseña = models.CharField(max_length=128, null=True, blank=True)  # Nuevo campo

    def __str__(self):
        return f"{self.nombre} ({self.especialidad})"

    def set_password(self, raw_password):
        self.contraseña = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contraseña)


class Hora(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="horas")
    fecha = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {'Disponible' if self.disponible else 'Reservada'}"
    


class Usuario(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    grupo = models.CharField(max_length=20, choices=[('Paciente', 'Paciente'), ('Medico', 'Medico')])

    def __str__(self):
        return self.username