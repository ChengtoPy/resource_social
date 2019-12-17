from django.conf.urls import url

from .views import IndexView, GoodClass, EnjoyView

app_name='srik'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^goodclass/$', GoodClass.as_view(), name="goodclass"),
    url(r'^enjoy/$',EnjoyView.as_view(),name="enjoy")
]