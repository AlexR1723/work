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
    url(r'^$', views.Main, name="Main"),
    url(r'^how_it_work/$', views.How_it_work, name="How_it_work"),
    url(r'^secure_transaction/$', views.Secure_transaction, name="Secure_transaction"),
    url(r'^safety/$', views.Safety, name="Safety"),
    url(r'^rabota/$', views.Rabota, name="Rabota"),
    url(r'^for_business/$', views.For_business, name="For_business"),
    url(r'^top_performers/$', views.Top_performers, name="Top_performers"),
    url(r'^login/$', views.Login, name="Login"),
    url(r'^register/$', views.Register, name="Register"),
    # url(r'^test/$', views.Test, name="Test"),

    url(r'^dev/$', views.Dev, name="Dev"),
]
