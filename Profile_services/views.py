from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
# Create your views here.
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



def Service(request):
    layout, username, photo, balance, bonus = layout_name(request)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            # us = request.session.get('username')
            service=Services.objects.filter(exec = True)
        else:
            service=Services.objects.exclude(exec = True)
    return render(request, 'Profile/Services.html', locals())


def Service_detail(request,id):
    layout, username, photo, balance, bonus = layout_name(request)
    id=int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        service = Services.objects.get(id=id)
        service_image=ServicesImage.objects.filter(service=service)
    return render(request, 'Profile/Service_details.html', locals())
