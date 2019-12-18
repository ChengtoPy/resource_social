from django.conf.urls import url

from .views import IndexView, GoodClass, EnjoyView, BwView, BcView, AnswerView, GetView, VipView, CommentView, \
    QuestionView

app_name='srik'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^goodclass/$', GoodClass.as_view(), name="goodclass"),
    url(r'^enjoy/$',EnjoyView.as_view(),name="enjoy"),
    url(r'^bw/$',BwView.as_view(),name='bw'),
    url(r'^bcym/$',BcView.as_view(),name='bc'),
    url(r'^answer/$',AnswerView.as_view(),name='answer'),
    url(r'^getcoin/$',GetView.as_view(),name='get'),
    url(r'^vip/$',VipView.as_view(),name='vip'),
    url(r'^comment/$',CommentView.as_view(),name='comment'),
    url(r'^question/$',QuestionView.as_view(),name='question'),
]