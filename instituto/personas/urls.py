
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns=[
    path("index", views.index, name="index"),
    path('listamedicos', views.listamedicos, name='listamedicos'),
    path('ver_horas_medico/<int:medico_id>/', views.ver_horas_medico, name='ver_horas_medico'),
    path('reservar_hora/<int:hora_id>/', views.reservar_hora, name='reservar_hora'),
    path('reservar_hora/<int:hora_id>/', views.reservar_hora, name='reservar_hora'),
    path('ver_citas', views.ver_citas_paciente, name='ver_citas_paciente'),
    path('ver_horas_pacientes', views.ver_horas_pacientes_medico, name='ver_horas_pacientes_medico'),
    path('login', views.login_usuario, name='login'),
    path('logout', views.logout_usuario, name='logout'),
    path('ruta_protegida/', views.vista_protegida, name='vista_protegida'),
    path('registro', views.registro_usuario, name='registro'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)