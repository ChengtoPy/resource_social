from django.conf.urls import url

from apps.other.views import SourceView

app_name='other'
urlpatterns = [
    url(r'^other/source/$', SourceView.as_view(), name="source"),
]