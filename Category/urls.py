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
    url(r'^$', views.All_category, name="All_category"),
    url(r'^sub_category/(?P<name>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.sub_category, name="sub_category"),
    url(r'^sub_category/(?P<name>[А-Яа-я\s0-9-()/a-z,:]+)/(?P<page>[0-9]+)/$', views.Page_subcategory, name="Page_subcategory"),
    url(r'^(?P<name>[А-Яа-я\s0-9-()/a-z,:]+)/$', views.Category_item, name="Category_item"),
    # url(r'questions/(?P<text>[А-Яа-я\s0-9-(),.?!/:;"”#№$%*+]+)/$', views.questions, name="questions"),
]
