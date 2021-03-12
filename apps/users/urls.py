from django.urls import path
from apps.users.views import *
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', TemplateView.as_view(
        template_name='users/welcome.html'), name='welcome'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(LogOutView.as_view()), name='logout'),
    path('misturnos/', login_required(MisTurnosView.as_view()), name='misturnos'),
    path('registrar/', RegistrarView.as_view(), name='registrar'),
    path('solicitarturno/', login_required(SolicitarTurnoView.as_view()),
         name="solicitarturno"),
    path('miperfil/', login_required(MiPerfilView.as_view()), name='miperfil'),
    path('modificarturno/', login_required(ModificarTurnoView.as_view()),
         name="modificarturno"),
    path('modificarturno/<id>/', login_required(ModificarTurnoView.as_view()), name='modificarturno'),
    path('index/', login_required(IndexView.as_view()), name="index"),
    path('check_matricula/',
         login_required(check_matricula), name="check_matricula"),


]
