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
    url(r'^newbies/$', views.Newbies, name="Newbies"),
    url(r'^how_it_work/$', views.How_it_work, name="How_it_work"),
    url(r'^secure_transaction/$', views.Secure_transaction, name="Secure_transaction"),
    url(r'^safety/$', views.Safety, name="Safety"),
    url(r'^rabota/$', views.Rabota, name="Rabota"),
    url(r'^for_business/$', views.For_business, name="For_business"),
    url(r'^pro_performers/(?P<name>[А-Яа-я\s0-9-()/a-zA-Z,:]+)/$', views.Pro_performers, name="Pro_performers"),
    url(r'^top_performers/$', views.Top_performers, name="Top_performers"),

    url(r'^login/$', views.Login, name="Login"),
    url(r'^register/$', views.Register, name="Register"),
    url(r'registrate/', views.Registrate),
    url(r'^forgot/', views.Forgot, name="Forgot"),
    url(r'send_new_pass/', views.send_new_pass),
    url(r'^verify/(?P<key>[a-z0-9]+)/$', views.Verify, name="Verify"),

    # url(r'find/(?P<text>[А-Яа-я\s0-9]+)/$', views.Find_category, name="Find_category"),

    url(r'^public_offer/$', views.Public_offer, name="Public_offer"),
    url(r'^rules/$', views.Rules, name="Rules"),
    url(r'^privacy_rules/$', views.Privacy_rules, name="Privacy_rules"),


    # url(r'^question_details/$', views.Question_details, name="Question_details"),
    # url(r'^sub_category/$', views.Sub_category, name="Sub_category"),
    # url(r'^services/$', views.Profile_services, name="Profile_services"),
    # url(r'^task_details/$', views.Task_details, name="task_details"),
    url(r'^task_details_performer/$', views.Task_details_performer, name="task_details_performer"),


    url(r'login_user', views.login_user, name='login_user'),
    url(r'search_input_category', views.search_input_category, name='search_input_category'),
    url(r'/set_session_city/', views.set_session_city, name='set_session_city'),
    url(r'get_counter_values', views.get_counter_values, name='get_counter_values'),

    url(r'^dev/$', views.Dev, name="Dev"),
    url(r'^413/$', views.handler413, name="handler413"),
    url(r'^page/$', views.Page, name="Page"),
    # url(r'^profile_verified/$', views.Profile_verified, name="profile_verified"),
    # url(r'^awards/$', views.Awards, name="awards"),
    # url(r'^number_verification/$', views.Number_verification, name="number_verification"),
    # url(r'^passport_verification/$', views.Passport_verification, name="passport_verification"),
    url(r'^service_details/$', views.Service_details, name="service_details"),
    url(r'^user_reviews/$', views.User_reviews, name="user_reviews"),
    # url(r'^private_messages/$', views.Private_messages, name="private_messages"),
    url(r'^chat/$', views.Chat, name="chat"),
    url(r'^comment_save', views.Comment_save, name='Comment_save'),
    # url(r'^dev/(?P<text>[А-Яа-я\s0-9-()/a-z,]+)/$', views.Dev, name="Dev"),
]
