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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'', include('Main.urls')),
    url(r'about/', include('About.urls')),
    url(r'category/', include('Category.urls')),
    url(r'help/', include('Help.urls')),
    url(r'contact/', include('Contact.urls')),
    url(r'news/', include('News.urls')),
    url(r'profile/', include('Profile.urls')),
    url(r'profile/advert/', include('Profile_advert.urls')),
    url(r'profile/task/', include('Profile_task.urls')),
    url(r'profile/offer/', include('Profile_offer.urls')),
    url(r'profile/balance/', include('Profile_balance.urls')),
    url(r'profile/message/', include('Profile_message.urls')),
    url(r'profile/notice/', include('Profile_notice.urls')),
    url(r'adverts/', include('Advert.urls')),
    url(r'tasks/', include('Task.urls')),
    url(r'service/', include('Services.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
