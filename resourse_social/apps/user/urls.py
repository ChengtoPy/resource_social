from django.conf.urls import url
from django.urls import re_path

from .views import LoginView, RegisterView, PassWordView, LogoutView, UserCenter

app_name='user'


urlpatterns = [
    url(r'^user/login/$', LoginView.as_view(), name="login"),
    url(r'^user/register/$', RegisterView.as_view(), name="register"),
    url(r'^user/forget/$',PassWordView.as_view(),name="forget"),
    url(r'^user/logout/$',LogoutView.as_view(),name="logout"),
    url(r'^user/ucenter/$',UserCenter.as_view(),name="center")
]