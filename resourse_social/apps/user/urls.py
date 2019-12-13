from django.conf.urls import url
from django.urls import re_path

from .views import LoginView, RegisterView

app_name='user'


urlpatterns = [
    url(r'^user/login/$', LoginView.as_view(), name="login"),
    url(r'^user/register/$', RegisterView, name="register"),
]