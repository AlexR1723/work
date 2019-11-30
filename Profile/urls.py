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
    url(r'^settings/$', views.Profile_settings, name="Profile_settings"),
    url(r'^choose_city/$', views.Choose_city, name="Choose_city"),
    url(r'^choose_categ/$', views.Choose_categ, name="Choose_categ"),
    url(r'^adverts_add/$', views.Adverts_add, name="Adverts_add"),


    url(r'change_password', views.change_password, name='change_password'),
    url(r'get_new_order', views.get_new_order, name='get_new_order'),
    url(r'get_notice_status', views.get_notice_status, name='get_notice_status'),
    url(r'get_status', views.get_status, name='get_status'),
]
