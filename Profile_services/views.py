from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
import json, datetime, calendar
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

def for_new_user(request):
    layout, username, photo, balance, bonus = layout_name(request)
    return render(request, 'Profile/Services.html', locals())

def tuktuk(request):
    fun1 = ftry(check_services)
    fun2 = ftry(check_pro)
    fun3 = check_top()
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

def add_award(top,string_top):
    print(top)
    awards = Awards_model.objects.get(backend_name=string_top)
    user_award = list(UserAwards.objects.filter(awards__backend_name=string_top).values_list('user_id', flat=True))
    print(user_award)
    for t in top:
        if t not in user_award:
            award = UserAwards(user_id=t, awards=awards, date=datetime.datetime.today())
            award.save()




def check_top():
    print('ok')
    # users = Users.objects.filter(type__name='Исполнитель')
    users = Users.objects.all()
    user_dict = {}
    print(users)
    for user in users:
        successful_comment = UserComment.objects.filter(user=user.auth_user).filter(quality__gte=4).filter(
            politeness__gte=4).filter(punctuality__gte=4).count()
        all_comment = UserComment.objects.filter(user=user.auth_user).count()
        com_percent = 0
        if all_comment > 0:
            com_percent = int((successful_comment * 100) / all_comment)
        user_dict[user.auth_user.id] = com_percent
    print(user_dict)
    list_d = list(user_dict.items())
    list_d.sort(key=lambda i: i[1], reverse=True)
    len_list = len(list_d)
    list_top_10 = []
    list_top_50 = []
    list_top_100 = []
    if len_list >= 10:
        list_top_10 = list_d[0:10]
        if len_list >= 50:
            list_top_50 = list_d[10:50]
            if len_list >= 100:
                list_top_100 = list_d[50:100]
            else:
                list_top_100 = list_d[50:]
        else:
            list_top_50 = list_d[10:]
    else:
        list_top_10 = list_d[0:]
    # print(list_top_10)
    # print(list_top_50)
    # print(list_top_100)
    top_10 = list(dict(list_top_10).keys())
    top_50 = list(dict(list_top_50).keys())
    top_100 = list(dict(list_top_100).keys())

    user=UserAwards.objects.filter(awards__backend_name='top_10_exec').filter(awards__backend_name='top_50_exec').filter(awards__backend_name='top_100_exec')
    for u in user:
        if u.user.id not in top_10 or u.user.id not in top_50 or u.user.id not in top_100:
            u.delete()

    add_award(top_10, 'top_10_exec')
    add_award(top_50, 'top_50_exec')
    add_award(top_100, 'top_100_exec')



    return True
