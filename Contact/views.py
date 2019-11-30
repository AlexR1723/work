from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from .models import *
from django.core.mail import send_mail


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
def Contact(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    return render(request, 'Contact/Contact.html', locals())

def Send(request):
    name = request.GET.get("name")
    email=request.GET.get("email")
    theme=request.GET.get("theme")
    mes=request.GET.get("message")
    message='Имя пользователя - '+ name + '\n'
    message=message + 'Email - '+ email + '\n'
    message=message + mes
    if (theme == ''):
        send_mail('Обратная связь', message, 'romanenko.anastasiya1998@yandex.ua',
                  ['romanenko.anastasiya1998@yandex.ua'], fail_silently=False)
    else:
        send_mail(theme, message, 'romanenko.anastasiya1998@yandex.ua',
                  ['romanenko.anastasiya1998@yandex.ua'], fail_silently=False)
    return HttpResponse(json.dumps({'data': 'ok'}))