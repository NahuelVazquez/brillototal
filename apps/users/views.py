from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.shortcuts import render, reverse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from apps.users.models import Cliente


# Clase para el login
class LoginView(View):

    template_name = "users/login.html"
    template_mis_turnos = "users/misturnos.html"
   
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
  
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            request.user=user 
            return HttpResponseRedirect(reverse('misturnos'))
            
            
        return render(request, self.template_name, context={'error':'USER Y/O PASSWORD INCORRECTO'})
           

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
        user = User.objects.create_user(username=usuario, email=email, password=password, first_name=nombre, last_name=apellido)
        telefono = int(request.POST.get('telefono'))
        cliente = Cliente.objects.create(telefono=telefono, usuario=user)
        request.user=user
        return HttpResponseRedirect(reverse('misturnos'))
        # to do SIEMPRE TIRA USUARIO "MARCO"

class MisTurnosView(View):
    
    template_name = "users/misturnos.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
    
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name)
