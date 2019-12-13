import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.user.models import Users


class LoginView(View):
    """用户登录请求"""

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        userlist = Users.objects.all()
        for var in userlist:
            if var.username == username and var.password == password:
                request.session['islogin'] = True
                request.session['username'] = username
                request.session['user_id'] = var.userid
                return JsonResponse({'res': 0, 'jump_url': "{% url 'srik:index' %}"})
            else:
                continue
        return JsonResponse({'res': 1, 'errmsg': '登录失败'})


class RegisterView(View):
    """用户注册请求"""

    def get(self, request):
        return render(request, 'users/register.html', {'errmsg': ''})

    def post(self, request):
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


class PassWordView(View):
    """修改密码"""

    def get(self, request):
        return render(request, 'users/user_center_order.html')


class LogoutView(View):
    """退出登录"""
    def get(self, request):
        request.session['islogin'] = False
        del request.session['username']
        del request.session['user_id']
        # 跳转到首页
        return render(request, 'users/login.html')
# Create your views here.
