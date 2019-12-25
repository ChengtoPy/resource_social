from django.conf.urls import url
from .views import get_token
from django.urls import path
urlpatterns = [
    url(r'^token/$',get_token,name='token')
]
