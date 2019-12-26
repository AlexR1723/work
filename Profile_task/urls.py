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


    url(r'^create/(?P<text>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Create_task, name="Create_task"),
    url(r'subcategory_find/', views.SubcategoryFind),
    url(r'save_task/', views.Save_task, name='Save_task'),
    #
    # url(r'get_new_order', views.get_new_order, name='get_new_order'),
    #
    url(r'^$', views.Profile_tasks, name="Profile_tasks"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.Profile_task_detail, name="Profile_task_detail"),
    url(r'^(?P<page>[0-9]+)/$', views.Profile_task_page, name="Profile_task_page"),
    url(r'^(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Profile_task_filter, name="Profile_task_filter"),
    url(r'^(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Profile_task_filter_page, name="Profile_task_filter_filter"),
    #
    # url(r'^executor_tasks/category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat, name="Executor_my_tasks_filter_cat"),
    # url(r'^executor_tasks/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_stat, name="Executor_my_tasks_filter_stat"),
    # url(r'^executor_tasks/category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat_stat, name="Executor_my_tasks_filter_cat_stat"),


]
