from django.conf.urls import url
from .views import get_token
from django.urls import path
app_name = 'qiniuyun'
urlpatterns = [
    url(r'^token/$',get_token,name='token')
]
