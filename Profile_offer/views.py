from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json,re
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from distutils.util import strtobool
import datetime


list_page = []
ads_count = 0
def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
def layout_name(request):
    layout = 'layout.html'
    username=''
    photo=''
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        photo=Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout,username,photo


def Offer(request):
    layout, username, photo = layout_name(request)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
    offers=UserOffer.objects.filter(advert__user_id=user).filter(is_accept=False)
    print(offers)

    return render(request, 'Profile/Offers.html', locals())

def accept_offer(request):
    email = request.session.get('username', 'no')
    if (email!='no' and Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
        # us = request.session.get('username')
        user = AuthUser.objects.get(username=email).id
        id=int(request.GET.get('id'))
        offer=UserOffer.objects.filter(advert_id=id).filter(advert__user_id=user)
        print(offer)
        print(offer[0].id)
        if len(offer)==0:
            return HttpResponse(json.dumps(False))
        else:
            offer[0].is_accept=True
            offer[0].save()
            return HttpResponse(json.dumps(True))