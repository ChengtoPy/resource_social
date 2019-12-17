from django.conf.urls import url

from apps.other.views import SourceView, BuyView

app_name='other'
urlpatterns = [
    url(r'^other/source/$', SourceView.as_view(), name="source"),
    url(r'^other/buy/$', BuyView.as_view(), name="buy"),
]