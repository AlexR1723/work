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
    url(r'^$', views.Advert, name="Advert"),
    url(r'^(?P<page>[0-9]+)/$', views.Advert_page, name="Advert_page"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.Adverts_detail, name="Adverts_detail"),
    # url(r'^advert_change/(?P<id>[0-9]+)/$', views.Adverts_change, name="Adverts_change"),
]
