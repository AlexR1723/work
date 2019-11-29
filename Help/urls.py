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
    url(r'^$', views.Help, name="Help"),
    url(r'^(?P<name>[А-Яа-я\s0-9]+)/$', views.Question_category, name="Question_category"),
    # url(r'^search_results/(?P<name>[А-Яа-я\s0-9]+)/$', views.Search_results, name="Search_results"),
    url(r'find_help/(?P<text>[А-Яа-я\s0-9]+)/$', views.Find_help, name="Find_help"),
    # url(r'^help_results/(?P<name>[А-Яа-я\s0-9]+)/$', views.Search_results_help, name="Search_results_help"),
    # url(r'^help_category/(?P<name>[А-Яа-я\s0-9]+)/$', views.Help_category, name="Help_category"),
    # url(r'^question_category/(?P<name>[А-Яа-я\s0-9]+)/$', views.Question_category, name="Question_category"),

    url(r'load_input_help', views.load_input_help, name='load_input_help'),
]
