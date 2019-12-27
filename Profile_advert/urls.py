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
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'add/', views.Advert_save, name='Advert_save'),
    url(r'^$', views.All_ads, name="All_ads"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.Advert_detail, name="Advert_detail"),
    url(r'^edit/(?P<id>[0-9]+)/$', views.Adverts_change, name="Adverts_change"),
    url(r'^(?P<page>[0-9]+)/$', views.All_ads_page, name="All_ads_page"),
    url(r'^(?P<filter>[А-Яа-я\s()-/a-z,:]+)/$', views.Advert_filter, name="Advert_filter"),
    url(r'^(?P<filter>[А-Яа-я\s()-/a-z,:]+)/(?P<page>[0-9]+)/$', views.Advert_filter_page,
        name="Advert_filter_page"),
    url(r'edit_advert', views.Edit_advert_save, name="Edit_advert_save"),
    url(r'user_delete_ads', views.user_delete_ads, name="user_delete_ads"),
]
