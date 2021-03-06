from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg,regions

def is_verify(request):
    if (request.session.get('username', 'no') != 'no'):
        verify = True
    else:
        verify = False
    return verify

def layout_name(request):
    layout = 'layout.html'
    username=''
    photo=''
    balance = 0
    bonus = 0
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        photo=Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        balance = user.balance
        bonus = user.bonus_balance
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout, username, photo, balance, bonus

# Create your views here.

def About_(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)
    verify = is_verify(request)

    who = About.objects.all().filter(type__name='Кто мы и что делаем?')
    mission = About.objects.all().filter(type__name='Наша миссия')
    story = About.objects.all().filter(type__name='История проекта')
    team = About.objects.all().filter(type__name='Команда')
    return render(request, 'About/About.html', locals())