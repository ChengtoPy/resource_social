from django.conf.urls import url
from django.urls import re_path

<<<<<<< HEAD
from .views import LoginView, RegisterView, PassWordView, LogoutView, UserCenter, PayvipView, UserInfoView, InfoModify
=======
from .views import LoginView, RegisterView, PassWordView, LogoutView, UserCenter, PayvipView, UserInfoView
>>>>>>> fe7fe06... 'feat:用户消息信息展示'

app_name='user'


urlpatterns = [
    url(r'^user/login/$', LoginView.as_view(), name="login"),
    url(r'^user/register/$', RegisterView.as_view(), name="register"),
    url(r'^user/forget/$',PassWordView.as_view(),name="forget"),
    url(r'^user/logout/$',LogoutView.as_view(),name="logout"),
    url(r'^user/ucenter/$',UserCenter.as_view(),name="center"),
    url(r'^user/pay/$',PayvipView.as_view(),name="pay"),
    url(r'^user/info/$',UserInfoView.as_view(),name="info"),
<<<<<<< HEAD
    url(r'^user/usermodify/$',InfoModify.as_view(),name="modify"),
=======
>>>>>>> fe7fe06... 'feat:用户消息信息展示'
]