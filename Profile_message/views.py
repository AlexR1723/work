from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, re
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from distutils.util import strtobool
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import os
from django.conf import settings
# from datetime import datetime
import datetime, pytz
from django.utils import dateformat, timezone
from django.db.models import Q
from django.utils.timezone import make_aware, make_naive, is_naive
from collections import Counter


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
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username = AuthUser.objects.all().filter(email=user)[0].first_name
        photo = Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout, username, photo


def format_time(time):
    year = datetime.date.today().year
    today=datetime.datetime.today().day
    if is_naive(time):
        time = make_aware(time)
    else:
        time = make_naive(time)
    if time.year == year:
        if time.day==today:
            return dateformat.format(time, "Сегодня в "+settings.TIME_FORMAT)
        else:
            return dateformat.format(time, settings.DATETIME_FORMAT)
    else:
        # print('another year')
        return dateformat.format(time, settings.LONG_DATETIME_FORMAT)


def get_user_id(request):
    user_id = request.session.get('username', False)
    try:
        user = AuthUser.objects.get(username=user_id).id
        return int(user)
    except:
        return False


def send_notice(request, text, is_executor):
    # all, exec, cust
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


@login_required()
def Personal_messages(request):
    layout, username, photo = layout_name(request)

    user_id = get_user_id(request)
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=False).order_by(
            #     'from_user',
            #     '-date').distinct(
            #     'from_user')
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=False).distinct(
            #     'from_user')
            # user_mess1 = PersonalMessage.objects.filter(to_user=user_id).filter(from_type_is_exec=False).distinct(
            #     'to_user')
            # user_mess = user_mess.union(user_mess1)
            # user_mess = user_mess.order_by('-date')
            user_mess = PersonalMessage.objects.filter(to_type_is_exec=False)
            user_mess1 = PersonalMessage.objects.filter(to_type_is_exec=False)
        else:
            user_mess = PersonalMessage.objects.filter(to_type_is_exec=True)
            user_mess1 = PersonalMessage.objects.filter(to_type_is_exec=True)

        user_mess = user_mess.filter(to_user=user_id).order_by('from_user', '-date')
        us_mess_list = user_mess.values_list('from_user', flat=True)
        user_mess1 = user_mess1.filter(from_user=user_id).exclude(to_user__in=us_mess_list).order_by('to_user', '-date')

        user_mess = user_mess.distinct('from_user')
        user_mess1 = user_mess1.distinct('to_user')
        user_mess = user_mess.union(user_mess1).order_by('-date')
        today = datetime.datetime.today().date()
        year = datetime.datetime.now().year

    return render(request, 'Profile/Private_messages.html', locals())


def check_messages(request):
    user_id = get_user_id(request)
    lst = []
    if request.GET.get('is_page') == 'true':
        is_page = True
    if request.GET.get('is_page') == 'false':
        is_page = False
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        try:
            with_user = int(request.GET.get('to_user'))
            me = int(request.GET.get('from_user'))
        except:
            with_user = False
            me = False
        mess = PersonalMessage.objects.filter(to_user=user_id).filter(is_show=False)
        if type_id == 1:
            mess = mess.filter(to_type_is_exec=False).select_related('from_user')
        else:
            mess = mess.filter(to_type_is_exec=True).select_related('from_user')
        # all_count = mess.count()
        all_count = mess.distinct('from_user').count()
        us_mess = []
        if is_page:
            users_mess = mess.distinct('from_user').order_by('from_user', '-date')
            for i in users_mess:
                us_item = []
                us_item.append(i.from_user.id)
                us_item.append(i.text)
                us_item.append(format_time(i.date))
                us_item.append(mess.filter(from_user=i.from_user).count())
                us_mess.append(us_item)

        if with_user and me:
            messages = PersonalMessage.objects.filter(Q(from_user=with_user) & Q(to_user=me) & Q(is_show=False))
            messages1 = messages.values_list('date', 'text')
            for i in messages1:
                item = []
                item.append(format_time(i[0]))
                item.append(i[1])
                lst.append(item)
            for i in messages:
                i.is_show = True
                i.save()

        return HttpResponse(json.dumps([all_count, us_mess, lst]))
    else:
        return HttpResponse(json.dumps([False, False, False]))


@login_required()
def Chat(request, with_user):
    layout, username, photo = layout_name(request)

    try:
        with_user = int(with_user)
    except:
        with_user = False

    user_id = get_user_id(request)
    if user_id and with_user:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
                to_type_is_exec=False)
            user_mess1 = PersonalMessage.objects.filter(to_user=with_user).filter(from_user=user_id).filter(
                from_type_is_exec=False)
            user_mess = user_mess.union(user_mess1)
            user_mess = user_mess.order_by('-date')
            if user_mess.count() == 0:
                return redirect('/profile/message/')
        else:
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
                to_type_is_exec=True)
            user_mess1 = PersonalMessage.objects.filter(to_user=with_user).filter(from_user=user_id)
            user_mess = user_mess.union(user_mess1)
            user_mess = user_mess.order_by('-date')
            if user_mess.count() == 0:
                return redirect('/profile/message/')

        with_user = AuthUser.objects.get(id=with_user)
        year = datetime.datetime.now().year
        today=datetime.datetime.today().day

        for i in user_mess:
            if i.is_show == False and i.to_user.id == user_id:
                i.is_show = True
                i.save()

    return render(request, 'Profile/Chat.html', locals())


@login_required()
def send_message(request):
    user_id = get_user_id(request)
    if user_id:
        try:
            mess = str(request.GET.get('message'))
            to_user = int(request.GET.get('user'))
        except:
            return HttpResponse(json.dumps(False))
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        from_user = AuthUser.objects.get(id=user_id)
        to_user = AuthUser.objects.get(id=to_user)
        if type_id == 1:
            send = PersonalMessage(from_user=from_user, to_user=to_user, text=mess, from_type_is_exec=False,
                                   to_type_is_exec=False, is_show=False, date=datetime.datetime.now())
            send.save()
            # if send:
            #     return HttpResponse(json.dumps([format_time(send.date), send.text]))
            # else:
            #     return HttpResponse(json.dumps(False))
        else:
            send = PersonalMessage(from_user=from_user, to_user=to_user, text=mess, from_type_is_exec=True,
                                   to_type_is_exec=True, is_show=False, date=datetime.datetime.now())
            send.save()
        if send:
            return HttpResponse(json.dumps([format_time(send.date), send.text]))
        else:
            return HttpResponse(json.dumps(False))
    else:
        return HttpResponse(json.dumps(False))
