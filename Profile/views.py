from django.shortcuts import render

# Create your views here.
def Profile_settings(request):
    return render(request, 'Profile/Profile_settings.html', locals())

def Choose_city(request):
    return render(request, 'Profile/Choose_city.html', locals())

def Adverts_add(request):
    return render(request, 'Profile/Adverts_add.html', locals())

def Choose_categ(request):
    return render(request, 'Profile/Choose_categ.html', locals())

from django.shortcuts import render

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

import json
import random
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password,make_password
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse



def change_password(request):
    old=request.GET.get('old')
    new1=request.GET.get('new1')
    new2=request.GET.get('new2')
    user_id=request.session['user_id']

    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    # check_sym=pattern_password.match()

    # user_id=29
    db_pass = AuthUser.objects.filter(id=user_id)
    # db_pass=AuthUser.objects.get(id=request.session['user_id'])
    # db_pass='grinya22041982'
    check=check_password(old, db_pass)
    if(check == True):
        # new1=make_password(new1)
        # new2=make_password(new2)
        if new1==new2:
            check_sym = pattern_password.match(new1)
            if check_sym==True:
                new1=make_password(new1)
                new2=make_password(new2)
                if new1==new2:
                    if new1!=db_pass:
                        AuthUser.objects.get(id=user_id).update(password=new1)
                        return HttpResponse(json.dumps('Пароли изменён'))
                    else:
                        return HttpResponse(json.dumps('Новый пароль должен отличаться от старого'))
                else:
                    return HttpResponse(json.dumps('Пароли не совпадают'))
            else:
                return HttpResponse(json.dumps('Пароли должен содержать только латинские буквы, заглавную букву и цифры!'))
        else:
            return HttpResponse(json.dumps('Пароли не совпадают'))
    else:
        return HttpResponse(json.dumps('Старый пароль неверный'))
    # pas1 = request.GET.get("pas1")
    # pas2 = request.GET.get("pas2")
    # pas3 = request.GET.get("pas3")
    # # id=request.session['userid']
    # # db_pas=AuthUser.objects.filter(id=request.session['userid'])
    # pas4 = AuthUser.objects.filter(id=request.session['userid'])[0].password
    # us = check_password(pas1, pas4)
    #
    # # print(us)
    # if (us == True):
    #     nw = make_password(pas3)
    #     print('1 if')
    #     if (pas2 == pas3):
    #         AuthUser.objects.filter(id=request.session['userid']).update(password=nw)
    #         return HttpResponse(json.dumps({'data': 'Пароль изменён'}))
    #     else:
    #         return HttpResponse(json.dumps({'data': 'Пароли не совпадают'}))
    # else:
    #     return HttpResponse(json.dumps({'data': 'Старый пароль неверный'}))
    # return HttpResponse(json.dumps('bad'))
