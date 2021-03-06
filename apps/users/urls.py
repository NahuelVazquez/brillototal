from django.urls import path
from apps.users.views import *
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='users/welcome.html'), name = 'welcome'),
    path('login/', LoginView.as_view(), name='login'),
    path('misturnos/', MisTurnosView.as_view(), name='misturnos'),
    path('registrar/', RegistrarView.as_view(), name='registrar'),
    path('solicitarturno/', SolicitarTurnoView.as_view(), name="solcitarturno"),
    path('miperfil/', MiPerfilView.as_view(), name='miperfil'),
    path('modificarturno/', ModificarTurnoView.as_view(), name="modificarturno"),
]