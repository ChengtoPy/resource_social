from django.conf.urls import url

from .views import IndexView, GoodClass

app_name='srik'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^goodclass/$', GoodClass.as_view(), name="goodclass"),
]