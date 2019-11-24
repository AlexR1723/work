from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
# Create your views here.

def About_(request):
    contact = layout_contact()
    link = layout_link()

    who = About.objects.all().filter(type__name='Кто мы и что делаем?')
    mission = About.objects.all().filter(type__name='Наша миссия')
    story = About.objects.all().filter(type__name='История проекта')
    team = About.objects.all().filter(type__name='Команда')
    return render(request, 'About/About.html', locals())