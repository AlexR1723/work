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
    url(r'^$', views.Personal_messages, name="Personal_messages"),
    url(r'^chat/(?P<chat_id>[0-9]+)/$', views.Chat, name="Chat"),
    # url(r'^personal_messages/$', views.Personal_messages, name="Personal_messages"),

    url(r'check_messages', views.check_messages, name='check_messages'),
    url(r'send_message', views.send_message, name='send_message'),
]
