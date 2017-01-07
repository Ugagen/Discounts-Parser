"""pars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?i)ios/', include('iOS.urls')),
    url(r'^(?i)android/', include('android.urls')),
    url(r'^(?i)Mac/', include('Mac.urls')),
    # url(r'^date(?P<date>.+)/$', sale.views.dates, name='dates'),
    # url(r'^date(?P<date>.+)/$', views.dates, name='dates'),
    # url(r'^polls/', include('polls.urls')),
    # url(r'^admin/', admin.site.urls),
]
