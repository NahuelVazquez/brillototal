from django.urls import path
from apps.users.views import LoginView
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='users/welcome.html'), name = 'welcome'),
    path('login/', LoginView.as_view(), name = 'login'),
]