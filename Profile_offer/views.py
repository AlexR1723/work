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


def Offer(request):
    layout, username, photo, balance, bonus = layout_name(request)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us)
            # offers=UserOffer.objects.filter(advert__user_id=user).filter(is_accept=False)
            offers=UserTask.objects.filter(offer__advert__user=user).filter(offer__is_accept=False)
            # print(offers)
            return render(request, 'Profile/Offers.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def accept_offer(request):
    email = request.session.get('username', 'no')
    if (email!='no' and Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
        # us = request.session.get('username')
        user = AuthUser.objects.get(username=email).id
        id=int(request.GET.get('id'))
        task=UserTask.objects.filter(id=id).filter(offer__advert__user_id=user)
        # print(task)
        # print(task[0].id)
        if len(task)==0:
            return HttpResponse(json.dumps(False))
        else:
            task[0].offer.is_accept=True
            task[0].offer.save()
            task[0].task_status=UserTaskStatus.objects.get(name="В работе")
            task[0].save()
            notice=Notifications(user=task[0].user, text="Ваше предложение принято!",
                                 date_public=datetime.datetime.now(), is_checked=False, is_show=False)
            notice.save()
            return HttpResponse(json.dumps(True))

def cancel_offer(request):
    email = request.session.get('username', 'no')
    if (email!='no' and Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
        # us = request.session.get('username')
        user = AuthUser.objects.get(username=email).id
        print(user)
        id=int(request.GET.get('id'))
        print(id)
        offer=UserOffer.objects.filter(id=id).filter(advert__user__id=user)
        print(offer)
        if len(offer) == 0:
            return HttpResponse(json.dumps(False))
        else:
            user=offer[0].user_id_customer
            notice=Notifications(user=offer[0].user_id_customer, text="Ваше предложение отклонено!",
                                 date_public=datetime.datetime.now(), is_checked=False, is_show=False)
            notice.save()
            task=UserTask.objects.filter(offer=offer[0])
            task.delete()
            offer.delete()
            return HttpResponse(json.dumps(True))
        # task=UserTask.objects.filter(id=id).filter(offer__advert__user_id=user)
        # print(task)
        # print(task[0].id)
        # if len(task)==0:
        #     return HttpResponse(json.dumps(False))
        # else:
        #     task[0].offer.is_accept=True
        #     task[0].offer.save()
        #     task[0].task_status=UserTaskStatus.objects.get(name="В работе")
        #     task[0].save()



def Offer_detail(request,id):
    layout, username, photo, balance, bonus = layout_name(request)
    id=int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        task=UserTask.objects.get(id=id)
        return render(request, 'Profile/Offer_details.html', locals())
        # task_bet = UserTaskBet.objects.filter(task=task).order_by('-date')
        # if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
        #     print('исполнитель')
        #     if (task.task_status.name=="В работе" and task.exec_finish != True):
        #         return render(request, 'Profile/Task_details_executor_work.html', locals())
        #     else:
        #         return render(request, 'Profile/Task_details_executor_finish.html', locals())
        # else:
        #     print(task.exec_finish)
        #     return render(request, 'Profile/Task_details.html', locals())

def check_count(request):
    user_id = request.GET.get("user_id")
    sub_name=request.GET.get('sub')
    user_pro=UserPro.objects.filter(user__id=user_id).filter(subcategory__name=sub_name).count()
    print(user_pro)
    if user_pro > 0:
        return HttpResponse(json.dumps({'data': 'ok'}))
    else:
        now=datetime.datetime.now()
        print(now)
        user_task=UserTask.objects.filter(subcategory__name=sub_name).filter(exec__id=user_id).filter(date_add=now).exclude(offer=None)
        print(user_task)
        if(user_task.count() < 3):
            return HttpResponse(json.dumps({'data': 'ok'}))
        else:
            return HttpResponse(json.dumps({'data': 'error'}))