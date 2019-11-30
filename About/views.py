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

# Create your views here.

def About_(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    who = About.objects.all().filter(type__name='Кто мы и что делаем?')
    mission = About.objects.all().filter(type__name='Наша миссия')
    story = About.objects.all().filter(type__name='История проекта')
    team = About.objects.all().filter(type__name='Команда')
    return render(request, 'About/About.html', locals())