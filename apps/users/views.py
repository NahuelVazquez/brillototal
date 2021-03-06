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
    
   
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
  
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            request.user=user 
            return HttpResponseRedirect(reverse('misturnos'))
            
            
        return render(request, self.template_name, context={'error':'USER Y/O PASSWORD INCORRECTO'})
           
#Clase para el registro del usuario
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
        
#Clase para visualizar los turnos
class MisTurnosView(View):
    
    template_name = "users/misturnos.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
        # to do SIEMPRE TIRA USUARIO "MARCO"
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('modificarturno'))

#Clase para solicitar un nuevo turno
class SolicitarTurnoView(View):
    
    template_name = "users/solicitarturno.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
    
    #FALTA DEFINIR VALORES INGRESADOS EN VARIABLES
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        vehiculo = request.POST.get('''# Que va acá''' ) 
        matricula = request.POST.get('matricula')
        metodo_pago = request.POST.get('''# Que va acá''')
        fecha = request.POST.get('fecha')
        horario = request.POST.get('''# Que va acá''')
        return HttpResponseRedirect(reverse('solicitarturno'))

#Clase para ver el perfil de usuario   
# falta implementar como se muestran los valores
class MiPerfilView(View):
    template_name = "users/miperfil.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
        # to do SIEMPRE TIRA USUARIO "MARCO"
    
    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('miperfil'))

#Clase para modificar los turnos
class ModificarTurnoView(View):
    
    template_name = "users/modificarturno.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, context={'user': request.user.username})
    
    #FALTA DEFINIR VALORES INGRESADOS EN VARIABLES
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        vehiculo = request.POST.get('''# Que va acá''' ) 
        matricula = request.POST.get('matricula')
        metodo_pago = request.POST.get('''# Que va acá''')
        fecha = request.POST.get('fecha')
        horario = request.POST.get('''# Que va acá''')
        return HttpResponseRedirect(reverse('modificarturno'))
    
    