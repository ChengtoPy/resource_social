from django.shortcuts import render
from django.views import View


class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')
# Create your views here.