from django.shortcuts import render
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
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout, username, photo


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
        # user_mess=PersonalMessage.objects.filter(to_user=user_id).distinct('from_user')

        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            #     messages = PersonalMessage.objects.filter(to_user=user.id).order_by('-date')
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=False).order_by(
                'from_user',
                '-date').distinct(
                'from_user')
        else:
            #     messages = PersonalMessage.objects.filter(to_user=user.id).order_by('-date')
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(to_type_is_exec=True).order_by(
                'from_user',
                '-date').distinct(
                'from_user')
        # print(user_mess[0])
        today = datetime.datetime.today().date()

    return render(request, 'Profile/Private_messages.html', locals())


def check_messages(request):
    user_id = get_user_id(request)
    if user_id:
        type_id = Users.objects.get(auth_user_id=user_id).type_id
        # mess = PersonalMessage.objects.filter(to_user=user_id).filter(is_checked=False).filter(is_show=False)
        mess = PersonalMessage.objects.filter(to_user=user_id).filter(is_show=False)
        if type_id == 1:
            count = mess.filter(to_type_is_exec=False).count()
        else:
            count = mess.filter(to_type_is_exec=True).count()
    else:
        count = 0
    return HttpResponse(json.dumps(count))


@login_required()
def Chat(request, with_user):
    layout, username, photo = layout_name(request)

    try:
        with_user = int(with_user)
    except:
        with_user = False

    user_id = get_user_id(request)
    if user_id and with_user:
        # user_mess=PersonalMessage.objects.filter(to_user=user_id).distinct('from_user')

        type_id = Users.objects.get(auth_user_id=user_id).type_id
        if type_id == 1:
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
            #     type_is_exec=False).order_by('date')
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
                to_type_is_exec=False)
            user_mess1 = PersonalMessage.objects.filter(to_user=with_user).filter(from_user=user_id)
            user_mess.union(user_mess1)
            print(user_mess)

        else:
            # user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
            #     type_is_exec=True).order_by('date')
            user_mess = PersonalMessage.objects.filter(to_user=user_id).filter(from_user=with_user).filter(
                to_type_is_exec=True)
            user_mess1 = PersonalMessage.objects.filter(to_user=with_user).filter(from_user=user_id)
            # print(user_mess)
            # print(user_mess1)
            user_mess = user_mess.union(user_mess1)
            user_mess = user_mess.order_by('date')
            # print(user_mess)
            # print(user_mess.count())

        with_user = AuthUser.objects.get(id=with_user)

        #
        # for i in user_mess:
        #     if i.is_show and not i.is_checked:
        #         # i.date=i.date
        #         i.is_checked = True
        #         i.save()
        for i in user_mess:
            if i.is_show == False:
                # i.date = i.date
                i.is_show = True
                i.save()

    return render(request, 'Profile/Chat.html', locals())
