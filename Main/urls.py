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
    url(r'^about/$', views.About, name="About"),
    url(r'^contact/$', views.Contact, name="Contact"),
    url(r'^news/$', views.News, name="News"),
    url(r'^news_detail/$', views.news_detail, name="news_detail"),
    url(r'^how_it_work/$', views.how_it_work, name="how_it_work"),
    url(r'^secure_transaction/$', views.secure_transaction, name="secure_transaction"),
    url(r'^safety/$', views.safety, name="safety"),
    url(r'^top/$', views.Top_performers, name="Top_performers"),
    url(r'^category/$', views.All_category, name="All_category"),
]
