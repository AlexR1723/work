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
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.Service, name="Service"),
    url(r'^(?P<id>[0-9]+)/$', views.Service_detail, name="Service_detail"),
    url(r'^task_add/(?P<id>[0-9]+)/$', views.Service_task_add, name="Service_task_add"),
    url(r'^add_service_in_task/$', views.Add_service_in_task, name="Add_service_in_task"),
    # url(r'^(?P<page>[0-9]+)/$', views.News_page, name="News_page"),
    # url(r'^(?P<filter>[А-Яа-я]+\s[А-Яа-я]+)/$', views.News_filter, name="News_filter"),
    # url(r'^(?P<filter>[А-Яа-я]+\s[А-Яа-я]+)/(?P<page>[0-9]+)/$', views.News_filter_page, name="News_filter_page"),
    # path('<slug:slug>', views.News_detail, name='News_detail'),
]
