from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
import json,datetime,calendar
from django.core.mail import send_mail

# Create your views here.
def layout_contact():
    contact = ContactType.objects.all()
    return contact


def layout_link():
    link = Link.objects.all()
    return link


def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg, regions


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


def Service(request):
    layout, username, photo, balance, bonus = layout_name(request)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            # us = request.session.get('username')
            service = Services.objects.filter(exec=True)
        else:
            service = Services.objects.exclude(exec=True)
    return render(request, 'Profile/Services.html', locals())


def Service_detail(request, id):
    layout, username, photo, balance, bonus = layout_name(request)
    id = int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        service = Services.objects.get(id=id)
        service_image = ServicesImage.objects.filter(service=service)
    return render(request, 'Profile/Service_details.html', locals())


def Service_task_add(request, id):
    layout, username, photo, balance, bonus = layout_name(request)
    id = int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        user = Users.objects.get(auth_user__email=email)
        service = Services.objects.exclude(exec=True)
        task = UserTask.objects.get(id=id)
        task_serv = TaskServices.objects.filter(task=task)
        select_serv = []
        select_serv_week = []
        select_serv_month = []
        for t in task_serv:
            select_serv.append(t.service_id)
            if t.week == True:
                select_serv_week.append(t.service_id)
            else:
                select_serv_month.append(t.service_id)
        print(select_serv)
        print(select_serv_week)
        print(select_serv_month)
        flag = 0
        aa = task.date
        bb = datetime.date.today()
        cc = aa - bb
        cc = str(cc)
        # print(cc)
        if (int(cc.split()[0]) > 2):
            service = service.exclude(back_name='quickly_task')
        # print(service)
        return render(request, 'Profile/Service_task_add.html', locals())


def Add_service_in_task(request):
    try:
        task_id = request.GET.get("task")
        service_id = request.GET.get("serv")
        time = request.GET.get("time")
        email = request.session.get('username', 'no')
        user = Users.objects.get(auth_user__email=email)
        task = UserTask.objects.get(id=task_id)
        service = Services.objects.get(id=service_id)
        if (time == 'week'):
            start = datetime.datetime.now()
            end = start
            end += datetime.timedelta(days=7)
            price = service.price_week
            print(end)
            task_service = TaskServices(task=task, service=service, start_date=start, end_date=end, week=True)
        else:
            start = datetime.datetime.now()
            end = start
            days_in_month = calendar.monthrange(start.year, start.month)[1]
            end += datetime.timedelta(days=days_in_month)
            price = service.price
            print(end)
            task_service = TaskServices(task=task, service=service, start_date=start, end_date=end, week=False)
        task_service.save()
        user.bonus_balance = user.bonus_balance - price
        user.save()
        return HttpResponse(json.dumps({'data': 'ok'}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))


def Service_advert_add(request, id):
    layout, username, photo, balance, bonus = layout_name(request)
    id = int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        user = Users.objects.get(auth_user__email=email)
        service = Services.objects.filter(exec=True).exclude(back_name='pro')
        advert = UserAdvert.objects.get(id=id)
        advert_serv = AdvertServices.objects.filter(advert=advert)
        select_serv = []
        select_serv_week = []
        select_serv_month = []
        for t in advert_serv:
            select_serv.append(t.service_id)
            if t.week == True:
                select_serv_week.append(t.service_id)
            else:
                select_serv_month.append(t.service_id)
        print(select_serv)
        print(select_serv_week)
        print(select_serv_month)
        flag = 0
        # aa = task.date
        # bb = datetime.date.today()
        # cc = aa - bb
        # cc = str(cc)
        # # print(cc)
        # if (int(cc.split()[0]) > 2):
        #     service = service.exclude(back_name='quickly_task')
        # print(service)
        return render(request, 'Profile/Service_advert_add.html', locals())


def Add_service_in_advert(request):
    try:
        advert_id = request.GET.get("advert")
        service_id = request.GET.get("serv")
        time = request.GET.get("time")
        email = request.session.get('username', 'no')
        user = Users.objects.get(auth_user__email=email)
        advert = UserAdvert.objects.get(id=advert_id)
        service = Services.objects.get(id=service_id)
        if (time == 'week'):
            start = datetime.datetime.now()
            end = start
            end += datetime.timedelta(days=7)
            price = service.price_week
            print(end)
            advert_service = AdvertServices(advert=advert, service=service, start_date=start, end_date=end, week=True)
        else:
            start = datetime.datetime.now()
            end = start
            days_in_month = calendar.monthrange(start.year, start.month)[1]
            end += datetime.timedelta(days=days_in_month)
            price = service.price
            print(end)
            advert_service = AdvertServices(advert=advert, service=service, start_date=start, end_date=end, week=False)
        advert_service.save()
        user.bonus_balance = user.bonus_balance - price
        user.save()
        return HttpResponse(json.dumps({'data': 'ok'}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))


def tuktuk(request):
    fun1 = ftry(check_services)
    fun2 = ftry(check_pro)
    return HttpResponse(json.dumps(True))


def ftry(func):
    try:
        data = datetime.datetime.now()
        # if data.hour == 0 and data.minute > 0 and data.minute < 30:
        f = func(data)
        # else:
        #     f=False
    except:
        f = False
    return f


def check_services(data):
    serv = TaskServices.objects.filter(end_date__lt=data.date())
    for i in serv:
        i.delete()
    return True

def check_pro(data):
    pros = UserPro.objects.filter(end_date__lt=data.date())
    for i in pros:
        i.delete()
    return True

def check_top(data):
    users = AuthUser.objects.all()
    user_dict = {}
    for user in users:
        successful_comment = UserComment.objects.filter(user=user).filter(quality__gte=4).filter(
            politeness__gte=4).filter(punctuality__gte=4).count()
        quality_suc = UserComment.objects.filter(user=user).filter(quality__gte=4).count()
        politeness_suc = UserComment.objects.filter(user=user).filter(politeness__gte=4).count()
        punctuality_suc = UserComment.objects.filter(user=user).filter(punctuality__gte=4).count()
        all_task = successful_comment.count()
        com_percent = 0
        if all_task > 0:
            com_percent = int((successful_comment * 100) / all_task)
        user_dict[com_percent] = user.id
    return True