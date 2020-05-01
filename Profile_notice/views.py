from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, re
from .models import *
import datetime
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from distutils.util import strtobool


def layout_contact():
    contact = ContactType.objects.all()
    return contact


def layout_link():
    link = Link.objects.all()
    return link


def layout_name(request):
    layout = 'layout.html'
    username = ''
    photo = ''
    balance = 0
    bonus = 0
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username = AuthUser.objects.all().filter(email=user)[0].first_name
        photo = Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        balance = user.balance
        bonus = user.bonus_balance
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout, username, photo, balance, bonus


def get_user_id(request):
    user_id = request.session.get('username', False)
    try:
        user = AuthUser.objects.get(username=user_id).id
        return int(user)
    except:
        return False


def Notice(request):
    layout, username, photo, balance, bonus = layout_name(request)
    # print(username)
    user_id = get_user_id(request)
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            notices = Notifications.objects.filter(user_id=user_id).exclude(for_executor=True).order_by('-date_public')
        else:
            notices = Notifications.objects.filter(user_id=user_id).exclude(for_executor=False).order_by('-date_public')
        today = datetime.datetime.today().date()
        for i in notices:
            if i.is_show and not i.is_checked:
                i.is_checked = True
                i.save()

        for i in notices:
            i.is_show = True
            i.save()
    return render(request, 'Profile/Notices.html', locals())


def send_notice(request, text, is_executor, user_id):
    if not user_id:
        user_id = request.session.get('username', False)
    try:
        user = AuthUser.objects.get(username=user_id).id
        if is_executor == 'exec':
            note = Notifications(user_id=user, text=text, for_executor=True, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        if is_executor == 'cust':
            note = Notifications(user_id=user, text=text, for_executor=False, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        if is_executor == 'all':
            note = Notifications(user_id=user, text=text, for_executor=None, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        note.save()
        print('note saved')
    except:
        return False


def check_notifications(request):
    user_id = get_user_id(request)
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        notes = Notifications.objects.filter(user_id=user_id).filter(is_checked=False).filter(is_show=False)
        if type_id == 1:
            count = notes.exclude(for_executor=True).count()
        else:
            count = notes.exclude(for_executor=False).count()
    else:
        count = 0
    return HttpResponse(json.dumps(count))
