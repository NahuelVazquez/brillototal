from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate


class LoginView(View):

    template_name = "users/login.html"
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
  
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user: 
            return HttpResponse(f'user {user.username}')
        
        return render(request, self.template_name, context={'error':'USER Y/O PASSWORD INCORRECTO'})
        
   
   







