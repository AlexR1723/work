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
import datetime
from django.db.models import Q


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
    layout, username, photo, balance, bonus = layout_name(request)

    user_id = get_user_id(request)
    if user_id:
        # user_mess=PersonalMessage.objects.filter(to_user=user_id).distinct('from_user')

        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=False).order_by(
            #     'from_user',
            #     '-date').distinct(
            #     'from_user')
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=False).distinct(
                'from_user')
            user_mess1 = PersonalMessage.objects.filter(to_user=user_id).filter(from_type_is_exec=False).distinct(
                'to_user')
            user_mess = user_mess.union(user_mess1)
            user_mess = user_mess.order_by('-date')
        else:
            #     messages = PersonalMessage.objects.filter(to_user=user.id).order_by('-date')
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=True).order_by(
            #     'from_user',
            #     '-date').distinct(
            #     'from_user')
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=True).distinct(
            #     'from_user')
            # print(user_mess)
            # user_mess1 = PersonalMessage.objects.filter(from_user=user_id).filter(from_type_is_exec=True).exclude(
            #     to_user__in=user_mess.values_list('from_user', flat=True))
            # .distinct(
            # 'to_user')
            # print(user_mess1)
            # user_mess = user_mess.union(user_mess1)
            # user_mess = user_mess.order_by('-date')
            # print(user_mess)
            # user_mess = PersonalMessage.objects.filter(to_type_is_exec=True).filter(Q(to_user=user_id) or Q(from_user=user_id))
            user_mess = PersonalMessage.objects.filter(to_type_is_exec=True).filter(to_user=user_id).order_by(
                'from_user', '-date')
            us_mess_list = user_mess.values_list('from_user', flat=True)
            user_mess1 = PersonalMessage.objects.filter(to_type_is_exec=True).filter(from_user=user_id).exclude(
                to_user__in=us_mess_list).order_by('to_user', '-date')

            user_mess = user_mess.distinct('from_user')
            user_mess1 = user_mess1.distinct('to_user')
            # print(user_mess)
            # print(user_mess1)
            user_mess = user_mess.union(user_mess1).order_by('-date')
            # print(user_mess)
        today = datetime.datetime.today().date()

    return render(request, 'Profile/Private_messages.html', locals())


def check_messages(request):
    user_id = get_user_id(request)
    lst = []
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        # print(request.GET.get('to_user'))
        # print(request.GET.get('from_user'))
        try:
            with_user = int(request.GET.get('to_user'))
            me = int(request.GET.get('from_user'))
        except:
            with_user = False
            me = False
        # mess = PersonalMessage.objects.filter(to_user=user_id).filter(is_checked=False).filter(is_show=False)
        mess = PersonalMessage.objects.filter(to_user=user_id).filter(is_show=False)
        if type_id == 1:
            count = mess.filter(to_type_is_exec=False).count()
        else:
            # count = mess.filter(to_type_is_exec=True).count()
            count = list(mess.filter(to_type_is_exec=True).values_list('from_user', flat=True))
            if with_user and me:
                messages = PersonalMessage.objects.filter(Q(from_user=with_user) & Q(to_user=me) & Q(is_show=False))

                messages1 = messages.values_list('date', 'text')
                # lst = []
                for i in messages1:
                    item = []
                    item.append(str(i[0]))
                    item.append(i[1])
                    lst.append(item)

                for i in messages:
                    i.is_show = True
                    i.save()
    else:
        count = 0
    return HttpResponse(json.dumps([count, lst]))


@login_required()
def Chat(request, with_user):
    layout, username, photo, balance, bonus = layout_name(request)

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
            if user_mess.count()==0:
                return redirect('/profile/message/')
        else:
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
                to_type_is_exec=True)
            user_mess1 = PersonalMessage.objects.filter(to_user=with_user).filter(from_user=user_id)
            user_mess = user_mess.union(user_mess1)
            user_mess = user_mess.order_by('-date')
            if user_mess.count()==0:
                return redirect('/profile/message/')

        with_user = AuthUser.objects.get(id=with_user)

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
            # count = mess.filter(to_type_is_exec=False).count()

            send = PersonalMessage(from_user=from_user, to_user=to_user, text=mess, from_type_is_exec=False,
                                   to_type_is_exec=False, is_show=False, date=datetime.datetime.now())
            send.save()
            if send:

                return HttpResponse(json.dumps([str(send.date), send.text]))
            else:
                return HttpResponse(json.dumps(False))
        else:

            send = PersonalMessage(from_user=from_user, to_user=to_user, text=mess, from_type_is_exec=True,
                                   to_type_is_exec=True, is_show=False, date=datetime.datetime.now())
            send.save()
            if send:

                return HttpResponse(json.dumps([str(send.date), send.text]))
            else:
                return HttpResponse(json.dumps(False))
    else:
        return HttpResponse(json.dumps(False))
