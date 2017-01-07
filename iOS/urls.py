from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^date(?P<date>.+)/$', views.dates, name='dates'),

]
