from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import *
from datetime import datetime


# Clase para el login
LONG_PASS = 8


class LoginView(View):

    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return render(request, self.template_name, context={'error': 'Username o password son nulos'})
        if len(password) < LONG_PASS:
            return render(request, self.template_name,
                          context={'error': f'El password debe ser mayor o igual a {LONG_PASS} caracteres'})
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        return render(request, self.template_name, context={'error': 'USER Y/O PASSWORD INCORRECTO'})


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('welcome'))


# Clase para el registro del usuario


class RegistrarView(View):

    template_name = "users/registrar.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        usuario = request.POST.get('usuario')
        user = User.objects.create_user(
            username=usuario, email=email, password=password, first_name=nombre, last_name=apellido)
        telefono = int(request.POST.get('telefono'))
        cliente = Cliente.objects.create(telefono=telefono, usuario=user)
        request.user = user
        return HttpResponseRedirect(reverse('index'))

# Clase para visualizar los turnos


class MisTurnosView(View):

    template_name = "users/misturnos.html"

    def get(self, request, *args, **kwargs):
        turnos = Turno.objects.filter(cliente__usuario=request.user)
        return render(request, self.template_name,
                      context={'user': request.user.username, 'turnos': turnos})
        # to do SIEMPRE TIRA USUARIO "MARCO"

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('modificarturno'))

# Clase para solicitar un nuevo turno


class SolicitarTurnoView(View):

    template_name = "users/solicitarturno.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,
                      context={'user': request.user.username, 'tipos_de_lavados': TIPO_LAVADO,
                               'tipo_de_vehiculos': TIPO_VEHICULO})

    # FALTA DEFINIR VALORES INGRESADOS EN VARIABLES
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        vehiculo = request.POST.get('vehiculo')
        lavado = request.POST.get('lavado')
        matricula = request.POST.get('matricula')
        fecha = request.POST.get('fecha')+'-'+request.POST.get('horario')
        horario = request.POST.get('horario')
        import pdb
        pdb.set_trace()

        lavado_object = Lavado.objects.get(tipo_lavado=lavado)
        vehiculo_object = Vehiculo.objects.create(
            tipo_vehiculo=vehiculo, matricula=matricula, )
        turno = Turno.objects.create(
            lavado=lavado_object,
            cliente__usuario=request.user,
            fecha=datetime.strptime(fecha, '%Y-%m-%d-%H:%M'),
            vehiculo=vehiculo_object)
        return HttpResponseRedirect(reverse('misturnos'))

# Clase para ver el perfil de usuario
# falta implementar como se muestran los valores


def check_matricula(request):
    if request.is_ajax():
        matricula = request.POST.get('matricula')
    return HttpResponse()


class MiPerfilView(View):
    template_name = "users/miperfil.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
        # to do SIEMPRE TIRA USUARIO "MARCO"

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('miperfil'))

# Clase para modificar los turnos


class ModificarTurnoView(View):

    template_name = "users/modificarturno.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})

    # FALTA DEFINIR VALORES INGRESADOS EN VARIABLES
    @ transaction.atomic
    def post(self, request, *args, **kwargs):
        vehiculo = request.POST.get('vehiculo')
        lavado = request.POST.get('lavado')
        matricula = request.POST.get('matricula')
        fecha = request.POST.get('fecha')
        horario = request.POST.get('horario')
        return HttpResponseRedirect(reverse('misturnos'))

# Clase para visualizar los turnos


class IndexView(View):

    template_name = "users/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
        # to do SIEMPRE TIRA USUARIO "MARCO"

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))
