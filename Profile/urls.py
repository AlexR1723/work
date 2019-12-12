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
    # url(r'^edit/$', views.Profile_edit, name="Profile_edit"),
    url(r'^choose_city/$', views.Choose_city, name="Choose_city"),
    url(r'^choose_categ/$', views.Choose_categ, name="Choose_categ"),
    url(r'^adverts_add/(?P<name>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Advert_add, name="Advert_add"),


    url(r'portfolio_save/', views.Portfolio_add, name='Portfolio_add'),
    url(r'delete_portfolio/', views.Delete_portfolio, name='Delete_portfolio'),
    url(r'save/', views.Save, name='Save'),
    # url(r'save_phone/', views.Save_phone, name='Save_phone'),
    url(r'save_photo/', views.Save_photo, name='Save_photo'),
    url(r'advert_add/', views.Advert_save, name='Advert_save'),
    url(r'^create_task/$', views.Create_task, name="Create_task"),
    url(r'subcategory_find/', views.SubcategoryFind),
    url(r'save_task/', views.Save_task, name='Save_task'),
    url(r'executor/', views.Executor),
    url(r'customer/', views.Customer),
    url(r'change_password', views.change_password, name='change_password'),
    url(r'get_new_order', views.get_new_order, name='get_new_order'),
    url(r'get_notice_status', views.get_notice_status, name='get_notice_status'),
    url(r'get_status', views.get_status, name='get_status'),
    # url(r'load_photos', views.load_photos, name='load_photos'),
    url(r'profile_set_subcategories', views.profile_set_subcategories, name='profile_set_subcategories'),
    url(r'profile_set_cities', views.profile_set_cities, name='profile_set_cities'),
    url(r'logout_user', views.logout_user, name='logout_user'),
    url(r'^adverts/$', views.All_ads, name="All_ads"),
    url(r'^adverts/(?P<page>[0-9]+)/$', views.All_ads_page, name="All_ads_page"),
    url(r'^adverts/(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Advert_filter, name="Advert_filter"),
    url(r'^adverts/(?P<filter>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Advert_filter_page, name="Advert_filter_page"),
    url(r'^advert_detail/(?P<id>[0-9]+)/$', views.Ads_details, name="Ads_details"),
    url(r'^my_tasks/$', views.My_tasks_customer, name="My_tasks_customer"),

    
]
