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
    url(r'^create_offer/(?P<id_advert>[0-9]+)/$', views.Offer_create, name="Offer_create"),
    url(r'subcategory_find/', views.SubcategoryFind),
    url(r'price_find/', views.PriceFind),
    url(r'sub_type_find/', views.SubTypeFind),
    url(r'save_task/', views.Save_task, name='Save_task'),
    url(r'save_offer/', views.Save_offer, name='Save_offer'),
    url(r'save_bet', views.Bet_save, name='Bet_save'),
    url(r'set_exec', views.Set_exec, name='Set_exec'),
    url(r'save_rezult', views.Rezult_task_save, name='Rezult_task_save'),
    url(r'^close_task/(?P<id>[0-9]+)', views.Close_task, name='Close_task'),
    #
    # url(r'get_new_order', views.get_new_order, name='get_new_order'),
    #
    url(r'^$', views.Profile_tasks, name="Profile_tasks"),
    url(r'^detail/(?P<id>[0-9]+)/$', views.Profile_task_detail, name="Profile_task_detail"),
    url(r'^(?P<page>[0-9]+)/$', views.Profile_task_page, name="Profile_task_page"),
    url(r'^(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Profile_task_filter, name="Profile_task_filter"),
    url(r'^(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Profile_task_filter_page, name="Profile_task_filter_filter"),
    #
    url(r'^category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Executor_my_tasks_filter_cat_page, name="Executor_my_tasks_filter_cat_page"),
    url(r'^category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat, name="Executor_my_tasks_filter_cat"),

    url(r'^stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Executor_my_tasks_filter_stat_page, name="Executor_my_tasks_filter_stat_page"),
    url(r'^stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_stat, name="Executor_my_tasks_filter_stat"),

    url(r'^category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Executor_my_tasks_filter_cat_stat_page, name="Executor_my_tasks_filter_cat_stat_page"),
    url(r'^category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat_stat, name="Executor_my_tasks_filter_cat_stat"),


]
