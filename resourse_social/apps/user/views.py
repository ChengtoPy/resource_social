import re

from django.shortcuts import render
from django.views import View

from apps.user.models import Users


class LoginView(View):
    def get(self,request):
        return render(request,'users/login.html')


class RegisterView(View):
    def get(self,request):
        return render(request, 'users/register.html', {'errmsg': ''})

    def post(self,request):
        print("post请求注册")
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        if not all([username, password, email]):
            # 有数据为空
            return render(request, 'users/register.html', {'errmsg': '参数不能为空!'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱不合法
            return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})
        if password != cpassword:
            return render(request, 'users/register.html', {'errmsg': '两次密码不一致!'})
        try:
            new_data = Users.objects.order_by('-id')[:1]
            if len(new_data) >= 1:
                newuid = new_data[0].userid + 1
                passport = Users(username=username, password=password, email=email, userid=newuid)
            else:
                passport = Users(username=username, password=password, email=email)
            passport.save()
        except Exception as e:
            print("e: ", e)  # 把异常打印出来
            return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})
        return render(request, 'users/login.html')
# Create your views here.
