"""work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.New, name="New"),
    url(r'^(?P<page>[0-9]+)/$', views.News_page, name="News_page"),
    url(r'^(?P<filter>[А-Яа-я]+\s[А-Яа-я]+)/$', views.News_filter, name="News_filter"),
    url(r'^(?P<filter>[А-Яа-я]+\s[А-Яа-я]+)/(?P<page>[0-9]+)/$', views.News_filter_page, name="News_filter_page"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.News_detail, name="News_detail"),
]
