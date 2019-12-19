import re

from django import http
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from apps.srik.models import Posts, Information
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
        if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{5,20}$', username):
            return render(request, 'users/register.html', {'errmsg': '用户名格式不对，需要5个字符及以上，禁止使用常用字符以外其他字符'})
        if not all([username, password, email]):
            # 有数据为空
            return render(request, 'users/register.html', {'errmsg': '参数不能为空!'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 邮箱不合法
            return render(request, 'users/register.html', {'errmsg': '邮箱不合法!'})
        if password != cpassword:
            return render(request, 'users/register.html', {'errmsg': '两次密码不一致!'})
        try:
            Users.objects.get(username=username)  # 判断用户名是否存在
            return render(request, 'users/register.html', {'errmsg': '用户名已存在！'})
        except Exception as e:
            print("e: ", e)  # 把异常打印出来
            try:
                Users.objects.get(email=email)  # 判断邮箱是否存在
                return render(request, 'users/register.html', {'errmsg': '邮箱已存在！'})
            except Exception as i:
                print("i: ", i)  # 把异常打印出来
                new_data = Users.objects.order_by('-id')[:1]
                if len(new_data) >= 1:
                    newuid = new_data[0].userid + 1

                    passport = Users(username=username, password=password, email=email, userid=newuid)
                else:
                    passport = Users(username=username, password=password, email=email)
                passport.save()
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


class UserCenter(View):
    """用户中心"""

    def get(self, request):
        user_info = Users.objects.get(username=request.session['username'])
        source = Posts.objects.filter(share_name=request.session['username'])
        info = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
        paginator = Paginator(source, 5)  # 每页显示25条数据

        page = request.GET.get('page', '1')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页面不是整数，则提交第一个页面。
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页面超出范围(例如9999)，则提交最后一页的结果。
            contacts = paginator.page(paginator.num_pages)

        context = {
            'zynum': len(source),
            'info_num': len(info),
            'contacts': contacts,
            'paginator': paginator,
            'user_info': user_info,
        }
        return render(request, 'users/user_center_info.html', context)


class PayvipView(View):
    """vip支付"""

    def get(self, request):
        return render(request, 'users/payvip.html')


class UserInfoView(View):
    """用户消息"""

    def get(self, request):
        user_info = Users.objects.get(username=request.session['username'])
        source = Posts.objects.filter(share_name=request.session['username'])

        info = Information.objects.filter(receive_name=request.session['username']).order_by('-send_time')
        info_n = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
        context = {
            'zynum': len(source),
            'info': info,
            'info_num': len(info_n),
            'user_info': user_info,
        }
        return render(request, 'users/user_info.html', context)
        # else:
        #     return JsonResponse({'res': 1, 'errmsg': '无效请求'})


class InfoModify(View):
    """用户信息修改"""

    def post(self, request):
        username_new = request.POST.get('username')
        username = request.session['username']  # 获取当前用户名
        des = request.POST.get('des')
        print(username_new)
        user_info = Users.objects.get(username=username)
        # 判断新用户名和旧用户名是否相同，新用户名是否为空,是否符合格式
        if username_new != username and len(username_new) != 0 and re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]{5,20}$', username_new):
            user_info.username = username_new
            request.session['username'] = username_new
        user_info.description = des
        user_info.save()
        return JsonResponse({'res': 0, 'errmsg': 'success'})

    # else:
    #     return JsonResponse({'res': 1, 'errmsg': '无效请求'})
    def get(self, request):
        if request.method == "GET":
            user_info = Users.objects.get(username=request.session['username'])
            source = Posts.objects.filter(share_name=request.session['username'])
            info = Information.objects.filter(receive_name=request.session['username']).order_by('-send_time')
            info_n = Information.objects.filter(receive_name=request.session['username'], read_sure=False)
            context = {
                'zynum': len(source),
                'info': info,
                'info_num': len(info_n),
                'user_info': user_info,
            }
            return render(request, 'users/user_info.html', context)
        else:
            return JsonResponse({'res': 1, 'errmsg': '无效请求'})
# Create your views here.
