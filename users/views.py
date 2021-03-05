from django.views import View
from django.http import HttpResponse



class LoginView(View):
    
    def get(self, request, *args, **kgars):
        return HttpResponse('LOGIN')
