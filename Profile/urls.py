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
    url(r'^$', views.Profile_page, name="Profile_page"),
    url(r'^settings/$', views.Profile_settings, name="Profile_settings"),
    url(r'^choose_city/$', views.Choose_city, name="Choose_city"),
    url(r'^choose_categ/$', views.Choose_categ, name="Choose_categ"),
    url(r'^awards/$', views.Awards, name="Awards"),
    url(r'^number_verification/$', views.Number_verification, name="Number_verification"),
    url(r'^adverts_add/(?P<name>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Advert_add, name="Advert_add"),


    url(r'portfolio_save/', views.Portfolio_add, name='Portfolio_add'),
    url(r'delete_portfolio/', views.Delete_portfolio, name='Delete_portfolio'),
    url(r'save/', views.Save, name='Save'),
    url(r'change_password', views.change_password, name='change_password'),
    url(r'save_photo/', views.Save_photo, name='Save_photo'),
    url(r'profile_set_subcategories', views.profile_set_subcategories, name='profile_set_subcategories'),
    url(r'profile_set_cities', views.profile_set_cities, name='profile_set_cities'),
    url(r'get_notice_status', views.get_notice_status, name='get_notice_status'),
    url(r'get_status', views.get_status, name='get_status'),
    url(r'verify_number', views.verify_number, name='verify_number'),

    url(r'executor/', views.Executor),
    url(r'customer/', views.Customer),
    # url(r'advert_add/', views.Advert_save, name='Advert_save'),

    # url(r'^create_task/(?P<text>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Create_task, name="Create_task"),
    # url(r'subcategory_find/', views.SubcategoryFind),
    # url(r'save_task/', views.Save_task, name='Save_task'),
    # url(r'get_new_order', views.get_new_order, name='get_new_order'),
    url(r'logout_user', views.logout_user, name='logout_user'),

    # url(r'^adverts/$', views.All_ads, name="All_ads"),
    # url(r'^adverts/detail/(?P<id>[0-9]+)/$', views.Advert_detail, name="Advert_detail"),
    # url(r'^adverts/(?P<page>[0-9]+)/$', views.All_ads_page, name="All_ads_page"),
    # url(r'^adverts/(?P<filter>[А-Яа-я\s()-/a-z,:]+)/$', views.Advert_filter, name="Advert_filter"),
    # url(r'^adverts/(?P<filter>[А-Яа-я\s()-/a-z,:]+)/(?P<page>[0-9]+)/$', views.Advert_filter_page, name="Advert_filter_page"),

    # url(r'^advert/edit/(?P<id>[0-9]+)/$', views.Adverts_change, name="Adverts_change"),
    # url(r'edit_advert' , views.Edit_advert_save,name="Edit_advert_save"),
    # url(r'user_delete_ads', views.user_delete_ads, name="user_delete_ads"),

    # url(r'^customer_tasks/$', views.Customer_my_tasks, name="Customer_my_tasks"),
    # url(r'^customer_tasks/(?P<page>[0-9]+)/$', views.Customer_tasks_page, name="Customer_tasks_page"),
    # url(r'^customer_tasks/(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.My_tasks_customer_filter, name="My_tasks_customer_filter"),
    # url(r'^customer_tasks/(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.My_tasks_customer_page_filter, name="My_tasks_customer_page_filter"),
    #
    # url(r'^executor_tasks/$', views.Executor_my_tasks, name="Executor_my_tasks"),
    # url(r'^executor_tasks/category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat, name="Executor_my_tasks_filter_cat"),
    # url(r'^executor_tasks/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_stat, name="Executor_my_tasks_filter_stat"),
    # url(r'^executor_tasks/category=(?P<filter_cat>[А-Яа-я\s0-9-()/a-z,:]+)/stat=(?P<filter_stat>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Executor_my_tasks_filter_cat_stat, name="Executor_my_tasks_filter_cat_stat"),


    url(r'^favorite_executors/$', views.Fav_executor, name="Fav_executor"),
    # url(r'^executor_tasks/$', views.Executor_my_tasks, name="Executor_my_tasks"),
    # url(r'^offers/$', views.Offer, name="Offer"),
    # url(r'accept_offer', views.accept_offer, name="accept_offer"),

]
