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
from django.contrib.auth.hashers import check_password, make_password
# from django.contrib.auth.hashers import *
import re
from django.contrib.auth.models import User

from distutils.util import strtobool

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse


def change_password(request):
    old = request.GET.get('old')
    new1 = request.GET.get('new1')
    new2 = request.GET.get('new2')

    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    db_pass = AuthUser.objects.get(id=user_id).password
    check = check_password(old, db_pass)

    if (check == True):
        if new1 == new2:
            check_sym = bool(pattern_password.match(new1))
            print(check_sym)
            if check_sym == True:
                if check_password(new1, db_pass) == False:
                    new_pass = make_password(new1)
                    # AuthUser.objects.filter(id=user_id).update(password=new_pass)
                    set_pass = AuthUser.objects.get(id=user_id)
                    set_pass.password = new_pass
                    set_pass.save()
                    # user =AuthUser.objects.get(id=user_id)
                    # user.set
                    # AuthUser.save(self)
                    # return HttpResponse(json.dumps('Пароли изменён!'))
                    return HttpResponse(json.dumps(True))
                else:
                    return HttpResponse(json.dumps('Новый пароль должен отличаться от старого!'))
            else:
                return HttpResponse(
                    json.dumps(
                        'Пароль должен содержать только латинские буквы, как минимум одну заглавную букву и цифру!'))
        else:
            return HttpResponse(json.dumps('Пароли не совпадают!'))
    else:
        return HttpResponse(json.dumps('Старый пароль неверный'))


def get_new_order(request):
    user = request.session.get('username', 0)
    print(user)
    status = bool(strtobool(request.GET.get('status')))
    print(status)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    set_status = Users.objects.get(auth_user=user_id)
    set_status.get_new_order = status
    set_status.save()
    if status == True:
        return HttpResponse(json.dumps('Теперь на вашу почту будет приходить рассылка заказов'))
    else:
        return HttpResponse(json.dumps('Рассылка заказов более приходить не будет'))


def get_notice_status(request):
    user = request.session.get('username', 0)
    print(user)
    status = bool(strtobool(request.GET.get('status')))
    print(status)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    set_status = Users.objects.get(auth_user=user_id)
    set_status.get_notice_status = status
    set_status.save()
    if status == True:
        return HttpResponse(
            json.dumps('Теперь на вашу почту будут приходить уведомления об изменениях статусов заказов'))
    else:
        return HttpResponse(json.dumps('Уведомления об изменениях статусов заказов более приходить не будут'))


def get_status(request):
    user = request.session.get('username', 0)
    print(user)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    get_status = Users.objects.get(auth_user=user_id)
    list = []
    list.append(get_status.get_notice_status)
    list.append(get_status.get_new_order)
    print(list)

    # time=request.session.get_expiry_age()
    # print(time/60/60/24)
    # date = request.session.get_expiry_date()
    # print(date)

    return HttpResponse(json.dumps(list))
    # response = HttpResponse({"error": "there was an error"})
    # response.status_code = 403  # To announce that the user isn't allowed to publish
    # return response

def load_photos(request):
    files=request.GET.get('files')
    print(files)

    return HttpResponse(json.dumps('good'))