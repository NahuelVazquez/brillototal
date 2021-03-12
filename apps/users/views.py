from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from apps.users.models import *


LONG_PASS = 8

# Clase para el login


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

# Administra el logout


class LogOutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('welcome'))


# Registro del usuario
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

# Muestra el perfil de usuario y permite modificar datos


class MiPerfilView(View):

    template_name = "users/miperfil.html"

    def get(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(usuario=request.user)
        return render(request, self.template_name,
                      context={'user': request.user, 'telefono': cliente.telefono})

    def post(self, request, *args, **kwargs):
        try:
            cliente = Cliente.objects.get(usuario=request.user)
            first_name = request.POST.get('nombre')

            if first_name:
                request.user.first_name = first_name
            second_name = request.POST.get('apellido')
            if second_name:
                request.user.second_name = second_name
            email = request.POST.get('email')
            if email:
                request.user.email = email
            telefono = request.POST.get('telefono')
            if telefono:
                cliente.telefono = telefono
            password = request.POST.get('password')
            if password:
                request.user.set_password(password)
            request.user.save()
            cliente.save()

        except Exception as e:
            return render(request, self.template_name,
                          context={'user': request.user, 'telefono': cliente.telefono, 'error': str(e)})

        return HttpResponseRedirect(reverse('index'))

    # AQUI CAMBIE COSAS
    def delete(self, request, usuario):
        usuario.delete()
        return render(request, self.template_name, {'user': usuario})

# Clase para visualizar los turnos


class MisTurnosView(View):

    template_name = "users/misturnos.html"

    def get(self, request, *args, **kwargs):
        fecha = request.POST.get('fecha')
        turnos = Turno.objects.filter(
            cliente__usuario=request.user).order_by("-fecha")

        return render(request, self.template_name,
                      context={'user': request.user.username, 'turnos': turnos})

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('modificarturno'))

# Clase para solicitar un nuevo turno


class SolicitarTurnoView(View):

    template_name = "users/solicitarturno.html"

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,
                      context={'user': request.user.username, 'tipos_de_lavados': TIPO_LAVADO,
                               'tipo_de_vehiculos': TIPO_VEHICULO})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lavado = request.POST.get('lavado')
        matricula = request.POST.get('matricula')
        fecha = request.POST.get('fecha')+'-'+request.POST.get('horario')
        horario = request.POST.get('horario')
        lavado_object = Lavado.objects.get(tipo_lavado=lavado)
        vehiculo_object = Vehiculo.objects.filter(matricula=matricula)
        cliente = Cliente.objects.get(usuario=request.user)
        if not vehiculo_object:
            marca = request.POST.get('marca')
            modelo = request.POST.get('modelo')
            tipo_vehiculo = request.POST.get('vehiculo')
            vehiculo_object = Vehiculo.objects.create(
                matricula=matricula,
                marca=marca,
                modelo=modelo,
                tipo_vehiculo=tipo_vehiculo,
                cliente=cliente)
        else:
            vehiculo_object = vehiculo_object.first()
        turno = Turno.objects.create(
            lavado=lavado_object,
            cliente=cliente,
            fecha=datetime.strptime(fecha, '%Y-%m-%d-%H:%M'),
            vehiculo=vehiculo_object)
        return HttpResponseRedirect(reverse('misturnos'))

# Clase para ver el perfil de usuario


@csrf_exempt
def check_matricula(request):
    if request.is_ajax():
        matricula = request.POST.get('matricula')
        if Vehiculo.objects.filter(matricula=matricula).exists():
            return HttpResponse("Existe")
        return HttpResponse("No existe")


# Clase para modificar los turnos
class ModificarTurnoView(View):

    template_name = "users/modificarturno.html"

    def get(self, request, *args, **kwargs):
        turno = Turno.objects.get(id=kwargs.get('id'))
        return render(request, self.template_name,
                      context={'user': request.user.username, 'tipos_de_lavados': TIPO_LAVADO,
                               'tipo_de_vehiculos': TIPO_VEHICULO, 'turno': turno})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        lavado = request.POST.get('lavado')
        matricula = request.POST.get('matricula')
        fecha = request.POST.get('fecha')+'-'+request.POST.get('horario')
        lavado_object = Lavado.objects.get(tipo_lavado=lavado)
        cliente = Cliente.objects.get(usuario=request.user)

        vehiculo_object = Vehiculo.objects.filter(matricula=matricula)
        if not vehiculo_object:
            marca = request.POST.get('marca')
            modelo = request.POST.get('modelo')
            tipo_vehiculo = request.POST.get('vehiculo')
            vehiculo_object = Vehiculo.objects.create(
                matricula=matricula,
                marca=marca,
                modelo=modelo,
                tipo_vehiculo=tipo_vehiculo,
                cliente=cliente)
        else:
            vehiculo_object = vehiculo_object.first()
            tipo_vehiculo = request.POST.get('vehiculo')
            marca = request.POST.get('marca')
            modelo = request.POST.get('modelo')
            if tipo_vehiculo:
                vehiculo_object.tipo_vehiculo = tipo_vehiculo
            if marca:
                vehiculo_object.marca = marca
            if modelo:
                vehiculo_object.modelo = modelo
            vehiculo_object.save()

        turno = Turno.objects.get(id=request.POST.get('id'))
        turno.lavado = lavado_object
        turno.fecha = datetime.strptime(fecha, '%Y-%m-%d-%H:%M')
        turno.vehiculo = vehiculo_object
        turno.save()

        return HttpResponseRedirect(reverse('misturnos'))

# Clase para visualizar los turnos


class IndexView(View):

    template_name = "users/index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
        # to do SIEMPRE TIRA USUARIO "MARCO"

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('index'))

# Falta Implementar clase que permite eliminar un turno


class EliminarTurnoView(View):
    pass
