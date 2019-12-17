from django.conf.urls import url

from .views import IndexView, GoodClass, EnjoyView, BwView

app_name='srik'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^goodclass/$', GoodClass.as_view(), name="goodclass"),
    url(r'^enjoy/$',EnjoyView.as_view(),name="enjoy"),
    url(r'^bw/$',BwView.as_view(),name='bw'),
]