from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json,re
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from distutils.util import strtobool
import datetime
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.db.models import Q


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

def send_notice(request, text, is_executor, user_id=False):
    # all, exec, cust
    if not user_id:
        user_id = request.session.get('username', False)
    try:
        user = AuthUser.objects.get(username=user_id).id
        if is_executor=='exec':
            note = Notifications(user_id=user, text=text, for_executor=True, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        if is_executor=='cust':
            note = Notifications(user_id=user, text=text, for_executor=False, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        if is_executor=='all':
            note = Notifications(user_id=user, text=text, for_executor=None, date_public=datetime.datetime.now(),
                                 is_checked=False, is_show=False)
        note.save()
        print('note saved')
    except:
        return False

def Profile_tasks(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    print('start')
    if username=='':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            us = request.session.get('username')
            user=AuthUser.objects.get(username=us).id
            filter=0
            all_user_task = task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True)
            task_count = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).order_by('-date').count()
            if (task_count < 10):
                task=UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).order_by('-date')[0:]
            else:
                task=UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).order_by('-date')[0:10]
            cats = []
            for i in all_user_task:
                el = SubCategory.objects.get(id=i.subcategory_id).name
                if el not in cats:
                    cats.append(el)
            cats.sort()
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            # fav_exec=UserFavoritesExecutor.objects.filter(user_id=user).order_by('-id')
            return render(request, 'Profile/My_tasks_customer.html', locals())
        else:

            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            filter_cat=0
            filter_stat=0
            list_cat = []
            for i in user_tasks:
                sub = i.subcategory.name
                if sub not in list_cat:
                    list_cat.append(sub)
            list_stat = UserTaskStatus.objects.all()
            list_cat.sort()
            task_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).order_by('-date').count()
            if (task_count < 10):
                task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).order_by('-date')[0:]
            else:
                task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).order_by('-date')[0:10]
            cats = []
            print(task)
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())



def Profile_task_page(request,page):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter = 0
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer=None, offer__is_accept=True)
            task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).order_by('-date').count()
            cats = []
            for i in user_tasks:
                el = SubCategory.objects.get(id=i.subcategory_id).name
                if el not in cats:
                    cats.append(el)
            cats.sort()
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            # fav_exec=UserFavoritesExecutor.objects.filter(user_id=user).order_by('-id')
            return render(request, 'Profile/My_tasks_customer.html', locals())
        else:
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            filter_cat = 0
            filter_stat = 0
            list_cat = []
            for i in user_tasks:
                sub = i.subcategory.name
                if sub not in list_cat:
                    list_cat.append(sub)
            list_stat = UserTaskStatus.objects.all()
            list_cat.sort()
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).order_by('-date').count()
            cats = []
            for i in user_tasks:
                el = SubCategory.objects.get(id=i.subcategory_id).name
                if el not in cats:
                    cats.append(el)
            cats.sort()
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            return HttpResponseRedirect("/profile/settings")

def Profile_task_filter(request,filter):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username=='':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            us = request.session.get('username')
            user=AuthUser.objects.get(username=us).id
            filter=str(filter)
            cat=SubCategory.objects.get(name__icontains=filter).id
            # subs_task=UserTask.objects.filter(user_id=user).filter(task_status=UserTaskStatus.objects.get(name='В работе').id).order_by('-date')
            all_user_task=task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True)
            task_count = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).filter(subcategory__id=cat).order_by('-date').count()
            if (task_count < 10):
                task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).filter(subcategory__id=cat).order_by('-date')[0:]
            else:
                task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).filter(subcategory__id=cat).order_by('-date')[0:10]
            cats = []
            for i in all_user_task:
                el = SubCategory.objects.get(id=i.subcategory_id).name
                if el not in cats:
                    cats.append(el)
            cats.sort()
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            print(cats)
            # fav_exec=UserFavoritesExecutor.objects.filter(user_id=user).order_by('-id')

        else:
            return HttpResponseRedirect("/profile/settings")
    return render(request, 'Profile/My_tasks_customer.html', locals())

def Profile_task_filter_page(request,filter,page):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter=str(filter)
            cat = SubCategory.objects.get(name__icontains=filter).id
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            all_user_task = task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True)
            task = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).filter(subcategory__id=cat).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(user_id=user).exclude(offer=None, offer__is_accept=True).filter(subcategory__id=cat).order_by('-date').count()
            cats = []
            for i in all_user_task:
                el = SubCategory.objects.get(id=i.subcategory_id).name
                if el not in cats:
                    cats.append(el)
            cats.sort()
            k = 0
            while (task_count > 0):
                k = k + 1
                task_count = task_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            # fav_exec=UserFavoritesExecutor.objects.filter(user_id=user).order_by('-id')

        else:
            return HttpResponseRedirect("/profile/settings")
    return render(request, 'Profile/My_tasks_customer.html', locals())

def Create_task(request,text):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if (username != ''):
        email = request.session.get('username', 'no')
        if(Users.objects.all().filter(auth_user__email=email)[0].type.name=='Заказчик'):
            category=Category.objects.all()
            city=City.objects.all()
            head=text
            print(head)
            return render(request, 'Profile/Create_task.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")
    else:
        return HttpResponseRedirect("/login")


def Offer_create(request, id_advert):
    print('offer')
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if (username != ''):
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            category = Category.objects.all()
            city = City.objects.all()
            id_advert=int(id_advert)
            advert=UserAdvert.objects.get(id=id_advert)
            print(advert)
            return render(request, 'Profile/Create_offer.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")
    else:
        return HttpResponseRedirect("/login")


def SubcategoryFind(request):
    try:
        cat = request.GET.get("id")
        subcategory=SubCategory.objects.all().filter(category__id=cat)
        subcategory_list = []
        for s in subcategory:
            subcategory_list.append(s.id)
            subcategory_list.append(s.name)
        price=subcategory[0].price
        return HttpResponse(json.dumps({'data': subcategory_list,'price':price}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))


def PriceFind(request):
    try:
        sub = request.GET.get("id")
        subcategory=SubCategory.objects.all().get(id=sub)
        price=subcategory.price
        return HttpResponse(json.dumps({'data': price}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))

def CheckBalance(request):
    try:
        price = request.GET.get("price")
        pay = request.GET.get("pay")
        email = request.session.get('username', 'no')
        user=Users.objects.get(auth_user__email=email)
        price=int(price)
        print(pay)
        if(pay == 1):
            if(user.balance>=price):
                return HttpResponse(json.dumps({'data': 'ok'}))
            else:
                return HttpResponse(json.dumps({'data': 'error'}))
        else:
            persent=price*10/100
            print(persent)
            if (user.balance >= persent):
                return HttpResponse(json.dumps({'data': 'ok'}))
            else:
                return HttpResponse(json.dumps({'data': 'error_1'}))
    except:
        return HttpResponse(json.dumps({'data': 'error_2'}))


def SubTypeFind(request):
    try:
        sub = request.GET.get("id")
        sub_type = SubcategoryType.objects.filter(subcategory_id=sub)
        sub_type_list=[]
        for i in sub_type:
            t=[]
            t.append(i.name)
            t.append(i.price)
            t.append(i.id)
            sub_type_list.append(t)
        return HttpResponse(json.dumps({'data': sub_type_list}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))


def Save_task(request):
    print('task_save')
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        sub = request.POST.get('subcategory')
        title = request.POST.get('task_title')
        description = request.POST.get('description')
        city = request.POST.get('city')
        address = request.POST.get('address')
        date_ = request.POST.get('date')
        gridRadios = request.POST.get('gridRadios')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        gridRadios2 = request.POST.get('gridRadios2')
        price = int(request.POST.get('input_price'))
        check=request.POST.get('pay_detail_check')
        is_pro=request.POST.get('is_pro')

        print(date_)
        date_ = date_.split('/')
        date = date_[2] + '-' + date_[0] + '-' + date_[1]
        print(date)
        pay = 1

        auth = AuthUser.objects.all().filter(email=email)[0]
        subcategory = SubCategory.objects.all().filter(id=sub)[0]
        status = UserTaskStatus.objects.get(name='В поиске')
        doc = request.FILES
        city = City.objects.all().filter(id=city)[0]
        # print (is_pro)
        # if is_pro == 1:
        #     is_pro=True
        # else:
        #     is_pro=False
        # print(is_pro)
        user = Users.objects.get(auth_user=auth)
        if (gridRadios2 == 'option1'):
            pay = 0
        if (gridRadios == 'option1'):
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     photo_main=doc['file_main'], task_status=status, date_add=datetime.datetime.now(),
                                     rezult_text="", is_pro=is_pro)
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price, task_status=status,
                                     date_add=datetime.datetime.now(), rezult_text="", is_pro=is_pro)
        else:
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, photo_main=doc['file_main'], task_status=status,
                                     date_add=datetime.datetime.now(), rezult_text="", is_pro=is_pro)
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, task_status=status, date_add=datetime.datetime.now(),
                                     rezult_text="", is_pro=is_pro)
        user_task.save()
        if user_task.pay:
            user.balance -= price
            user.frozen_balance += price
            user_balance=UserBalance(user=auth,sum=price,decription="Стоимость задания заморожена с Вашего счета до завершения задания", date=datetime.datetime.today())
            user_balance.save()
        else:
            print(price)
            user.balance -= (price * 10) / 100
            user.frozen_balance += price * 10 / 100
            user_balance = UserBalance(user=auth, sum = price * 10 / 100,
                                       decription="10% от стоимости задания заморожено с Вашего счета до завершения задания", date=datetime.datetime.today())
            user_balance.save()
        user.save()

        # выбираем всех пользователей с подкатегориями
        all_users=UserSubcategories.objects.filter(subcategories=subcategory)
        for i in all_users:
            us_s = Users.objects.get(auth_user=i.user)
            if us_s.get_new_order:
                em = settings.EMAIL_HOST_USER
                subject, from_email, to = 'Новое задание', em, i.user.email
                text_content = 'Перейдите по ссылке'
                # m = 'https://work-proj.herokuapp.com/verify/' + key
                # print(m)
                html_content = render_to_string('email_other_letter.html', {"title": "Новое задание",
                                                                            "text": "Появилось новое задание в категории "+subcategory.name+". Перейдите по ссылке ниже для получения подробной информации",
                                                                            "url": "http:/www.porabotaem.com/profile/task/detail/" + str(user_task.id), "url_text": user_task.title})
                print(html_content)
                # html_content="<a href='%s'>Активировать</a>" % m
                # html_content="<a href='%s'>Активировать</a>" % m
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

        if check != "":
            check_list=check.split('|')
            for i in check_list:
                if i != '':
                    sub_type=SubcategoryType.objects.get(id=i)
                    task_sub=TaskSubType(task=user_task, subtype=sub_type)
                    task_sub.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
    # return HttpResponseRedirect("/profile/task")
        user_task_id=user_task.id

        user_task=UserTask.objects.filter(user=auth)
        user_bonuses_count=UserBonuses.objects.filter(bonus__backend_name='create_3_tasks').count()
        bonus=""
        c_t=0
        if user_bonuses_count==0:
            if user_task.count() == 3:
                bonus=Bonuses.objects.get(backend_name='create_3_tasks')
                c_t=3
        else:
            user_bonuses_count = UserBonuses.objects.filter(bonus__backend_name='create_5_tasks').count()
            if user_bonuses_count == 0:
                if user_task.count() == 5:
                    bonus = Bonuses.objects.get(backend_name='create_5_tasks')
                    c_t=5
            else:
                user_bonuses_count = UserBonuses.objects.filter(bonus__backend_name='create_10_tasks').count()
                if user_bonuses_count == 0:
                    if user_task.count() == 10:
                        bonus = Bonuses.objects.get(backend_name='create_10_tasks')
                        c_t=10
            if bonus != "":
                user_bonuses=UserBonuses(bonus=bonus,user=auth)
                user_bonuses.save()
                user.bonus_balance+=bonus.count
                user.save()
                send_notice(request, "Вы получили бонус "+str(bonus.count)+" баллов за создание "+str(c_t)+" заданий!", "all")

        user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='create_10_tasks').count()
        award = ""
        if user_task.count() == 10:
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='create_10_tasks')
                c_t=10
        if user_task.count() == 50:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='create_50_tasks').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='create_50_tasks')
                c_t=50
        if user_task.count() == 100:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='create_100_tasks').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='create_100_tasks')
                c_t=100
        if award != "":
            user_award = UserAwards(user=auth, awards=award, date=datetime.datetime.now())
            user_award.save()
            bonus = Bonuses.objects.get(backend_name='reward_cust')
            user.bonus_balance += bonus.count
            user.save()
            send_notice(request,"Вы получили награду за создание " + str(c_t) + " заданий и бонус " + str(bonus.count) + " баллов!", "all")
    return HttpResponseRedirect("/profile/service/task_add/"+str(user_task_id))


def Save_offer(request):
    print('offer_save')
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        sub = request.POST.get('subcategory')
        print(sub)
        title = request.POST.get('task_title')
        description = request.POST.get('description')
        city = request.POST.get('city')
        address = request.POST.get('address')
        date_ = request.POST.get('date')
        gridRadios = request.POST.get('gridRadios')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        gridRadios2 = request.POST.get('gridRadios2')
        price = request.POST.get('input_price')
        advert_id = request.POST.get('advert_id')
        print(date_)
        date_ = date_.split('/')
        date = date_[2] + '-' + date_[0] + '-' + date_[1]
        print(date)
        pay = 1

        auth = AuthUser.objects.all().filter(email=email)[0]
        advert = UserAdvert.objects.get(id=advert_id)
        offer = UserOffer(user_id_customer=auth, advert=advert, is_accept=False, date=datetime.datetime.now())
        offer.save()
        subcategory = SubCategory.objects.all().filter(id=sub)[0]
        print(subcategory)
        # status = UserTaskStatus.objects.get(name='В поиске')
        exec_ = AuthUser.objects.get(id=advert.user.id)
        doc = request.FILES
        city = City.objects.all().filter(id=city)[0]
        if (gridRadios2 == 'option1'):
            pay = 0
        if (gridRadios == 'option1'):
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     photo_main=doc['file_main'], date_add=datetime.datetime.now(),
                                     offer=offer, exec=exec_, rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     date_add=datetime.datetime.now(), offer=offer, exec=exec_, rezult_text="")
        else:
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, photo_main=doc['file_main'],
                                     date_add=datetime.datetime.now(), offer=offer, exec=exec_, rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, date_add=datetime.datetime.now(),
                                     offer=offer, exec=exec_, rezult_text="")
        user_task.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
        advert.count_offer=advert.count_offer+1
        advert.save()
        notise=Notifications(user=exec_, text="У вас новое предложение. Проверьте страницу 'Предложения'",
                             date_public=datetime.datetime.now(), is_checked=False, is_show=False)
        notise.save()

        user_offer_count = UserTask.objects.filter(exec=exec_).count()
        user_award_count = UserAwards.objects.filter(user=exec_).filter(awards__backend_name='get_10_offers').count()
        award = ""
        c_o = 0
        if user_offer_count == 10:
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='get_10_offers')
                c_o = 10
        if user_offer_count == 20:
            user_award_count = UserAwards.objects.filter(user=exec_).filter(awards__backend_name='get_20_offers').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='get_20_offers')
                c_o = 20
        if user_offer_count == 50:
            user_award_count = UserAwards.objects.filter(user=exec_).filter(awards__backend_name='get_50_offers').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='get_50_offers')
                c_o = 50
        if award != "":
            user_award = UserAwards(user=exec_, awards=award, date=datetime.datetime.now())
            user_award.save()
            bonus = Bonuses.objects.get(backend_name='reward_exec')
            user = Users.objects.get(auth_user=exec_)
            user.bonus_balance += bonus.count
            user.save()
            send_notice(request,
                        "Вы получили награду за то, что получили " + str(c_o) + " предложений по своим объявлениям и бонус " + str(bonus.count) + " баллов!",
                        "all",user.auth_user.username)

    return HttpResponseRedirect("/profile/task")


def Profile_task_detail(request,id):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    id=int(id)
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        task=UserTask.objects.get(id=id)
        task_bet = UserTaskBet.objects.filter(task=task).order_by('-date')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            print('исполнитель')
            if (task.task_status.name=="В работе" and task.exec_finish != True):
                return render(request, 'Profile/Task_details_executor_work.html', locals())
            else:
                return render(request, 'Profile/Task_details_executor_finish.html', locals())
        else:
            print(task.exec_finish)
            return render(request, 'Profile/Task_details.html', locals())

def Bet_save(request):
    layout, username, photo, balance, bonus = layout_name(request)
    id=int(request.GET.get('id'))
    description=request.GET.get('description')
    sum=int(request.GET.get('sum'))
    hide=request.GET.get('hide')
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        print(email)
        auth=AuthUser.objects.get(email=email)
        print(auth)
        task=UserTask.objects.get(id=id)
        if hide == 'true':
            hide=True
        else:
            hide=False
        task_bet=UserTaskBet(user=auth, task=task, description=description, price=sum, date=datetime.datetime.now(), is_hide=hide)
        print(task_bet)
        task_bet.save()

        user_bet_count = UserTaskBet.objects.filter(user=auth).count()
        user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='bet_10').count()
        award = ""
        c_b=0
        if user_bet_count == 10:
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='bet_10')
                c_b=10
        if user_bet_count == 50:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='bet_50').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='bet_50')
                c_b=50
        if user_bet_count == 100:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='bet_100').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='bet_100')
                c_b=100
        if award != "":
            user_award = UserAwards(user=auth, awards=award, date=datetime.datetime.now())
            user_award.save()
            bonus = Bonuses.objects.get(backend_name='reward_exec')
            user = Users.objects.get(auth_user=auth)
            user.bonus_balance += bonus.count
            user.save()
            send_notice(request, "Вы получили награду за то, что оставили " + str(c_b) + " ставок и бонус " + str(bonus.count) + " баллов!", "all")
        return HttpResponse(json.dumps({'data': 'ok'}))


def Set_exec(request):
    layout, username, photo, balance, bonus = layout_name(request)
    id = int(request.POST.get('task_id'))
    user_id = int(request.POST.get('user_id'))
    mess=request.POST.get('text_mess')
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        auth=AuthUser.objects.get(email=email)
        user=AuthUser.objects.get(id=user_id)
        task=UserTask.objects.get(id=id)
        bet=UserTaskBet.objects.filter(task=task).filter(user=user)[0]
        task.task_status=UserTaskStatus.objects.get(name='В работе')
        task.exec=user
        task.price=bet.price
        print(task)
        task.save()

        chat=UserChat.objects.filter(from_user=auth).filter(to_user=user)|UserChat.objects.filter(from_user=user).filter(to_user=auth)
        if chat.count() == 0:
            chat=UserChat(from_user=auth, to_user=user)
            chat.save()
        else:
            chat=chat[0]
        print(chat)
        message=ChatMessage(chat=chat,user=auth,text=mess, date=datetime.datetime.now(), is_show=False)
        message.save()

        us_s=Users.objects.get(auth_user=user)
        if us_s.get_notice_status:
            em = settings.EMAIL_HOST_USER
            subject, from_email, to = 'Изменение статуса задания', em, user.email
            text_content = 'Перейдите по ссылке'
            # m = 'https://work-proj.herokuapp.com/verify/' + key
            # print(m)
            html_content = render_to_string('email_other_letter.html', {"title": "Изменение статуса задания", "text": "Вы назначены исполнителем для выполнения задания. Перейдите по ссылке ниже для получения подробной информации", "url": "http:/www.porabotaem.com/profile/task/detail/" + str(id), "url_text": task.title})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        # message=PersonalMessage(from_user=auth, to_user=user, text=mess, date=datetime.datetime.now(), is_show=False, to_type_is_exec=True, from_type_is_exec=True)
        # message.save()
        # return HttpResponse(json.dumps({'data': 'ok'}))
        return HttpResponseRedirect("/profile/task/detail/" + str(id))


def Executor_my_tasks_filter_cat(request,filter_cat):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_cat=str(filter_cat)

            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat = i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).count()
            if (user_tasks_count < 10):
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).order_by('-date')[0:]
            else:
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).order_by('-date')[0:10]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def Executor_my_tasks_filter_cat_page(request,filter_cat,page):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_cat=str(filter_cat)

            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat = i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).count()
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).order_by('-date')[start:end]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")


def Executor_my_tasks_filter_stat(request,filter_stat):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_stat=str(filter_stat)
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id)

            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat = i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).count()
            if (user_tasks_count < 10):
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[0:]
            else:
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[0:10]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def Executor_my_tasks_filter_stat_page(request,filter_stat,page):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_stat = str(filter_stat)

            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat = i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).count()
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[start:end]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def Executor_my_tasks_filter_cat_stat(request,filter_cat,filter_stat):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_stat=str(filter_stat)
            filter_cat=str(filter_cat)
            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat=i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).count()
            if (user_tasks_count < 10):
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[0:]
            else:
                user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[0:10]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            list_page = []
            page = 1
            if (k > 6):
                for i in range(1, 4):
                    list_page.append(i)
                list_page.append('...')
                for i in range(k - 2, k + 1):
                    list_page.append(i)
            else:
                for i in range(1, k + 1):
                    list_page.append(i)
            pre = 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def Executor_my_tasks_filter_cat_stat_page(request,filter_cat,filter_stat,page):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.filter(auth_user__email=email)[0].type.name == 'Исполнитель'):
            us = request.session.get('username')
            user = AuthUser.objects.get(username=us).id
            filter_stat = str(filter_stat)
            filter_cat = str(filter_cat)

            user_task = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False)
            list_cat = []
            list_stat = UserTaskStatus.objects.all()
            for i in user_task:
                cat = i.subcategory.name
                if cat not in list_cat:
                    list_cat.append(cat)
            list_cat.sort()
            page = int(page)
            start = page * 10 - 10
            end = page * 10
            user_tasks_count = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).count()
            user_tasks = UserTask.objects.filter(exec_id=user).exclude(offer__is_accept = False).filter(subcategory_id=SubCategory.objects.get(name__icontains=filter_cat).id).filter(task_status=UserTaskStatus.objects.get(name__icontains=filter_stat).id).order_by('-date')[start:end]
            k = 0
            while (user_tasks_count > 0):
                k = k + 1
                user_tasks_count = user_tasks_count - 10
            Page = []
            if k > 6:
                # записать первые 3
                for i in range(1, 4):
                    Page.append(i)
                # записать середину
                if page >= 3 and page <= (k - 2):
                    for i in range(page - 1, page + 2):
                        Page.append(i)
                # записать последние 3
                for i in range(k - 2, k + 1):
                    Page.append(i)
            else:
                for i in range(1, k + 1):
                    Page.append(i)
            # убрать повторения
            Page = list(set(Page))
            print(Page)
            list_page = []
            # добавить '...'
            for i in range(len(Page) - 1):
                list_page.append(Page[i])
                if Page[i + 1] - Page[i] > 1:
                    list_page.append('...')
            list_page.append(Page[len(Page) - 1])
            pre = page - 1
            next = page + 1
            return render(request, 'Profile/My_tasks_executor.html', locals())
        else:
            return HttpResponseRedirect("/profile/settings")

def Rezult_task_save(request):
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        id=request.POST.get('task_id')
        text = request.POST.get('task_rezult_text')
        auth = AuthUser.objects.all().filter(email=email)[0]
        task=UserTask.objects.get(id=id)
        task.rezult_text=text
        task.task_status=UserTaskStatus.objects.get(name="Завешено исполнителем")
        task.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_rezult_photo = UserTaskRezultPhoto(task=task, photo=d)
                tast_rezult_photo.save()

        us_s = Users.objects.get(auth_user=task.user)
        if us_s.get_notice_status:
            em = settings.EMAIL_HOST_USER
            subject, from_email, to = 'Изменение статуса задания', em, task.user.email
            text_content = 'Перейдите по ссылке'
            html_content = render_to_string('email_other_letter.html', {"title": "Завершено исполнителем",
                                                                        "text": "Выше задание завершено исполнителем. Перейдите по ссылке ниже для получения подробной информации",
                                                                        "url": "http:/www.porabotaem.com/profile/task/detail/" + str(task.id), "url_text": task.title})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    return HttpResponseRedirect("/profile/task")


def Close_task(request, id):
    layout, username, photo, balance, bonus = layout_name(request)
    if (username != ''):
        email = request.session.get('username', 'no')
        id=int(id)
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            task=UserTask.objects.get(id=id)
            task.task_status=UserTaskStatus.objects.get(name='Выполнено')
            task.save()
            cust_user=Users.objects.get(auth_user=task.user)
            exec_user=Users.objects.get(auth_user=task.exec)
            price=task.price
            if task.pay:
                cust_user.frozen_balance-=price
                cust_user.save()
                exec_user.balance+=price*90/100
                exec_user.save()
                user_balance=UserBalance(user=task.user,sum=price,decription="Списано с 'замороженого счета' при закрытии задания: "+task.title, date=datetime.datetime.today())
                user_balance.save()
                user_balance=UserBalance(user=task.exec,sum=price*90/100,decription="Зачислено на Ваш баланс при закрытии задания: "+task.title, date=datetime.datetime.today())
                user_balance.save()
            else:
                cust_user.frozen_balance -= price*10/100
                cust_user.save()
                user_balance=UserBalance(user=task.user,sum=price*10/100,decription="Списано с 'замороженого счета' при закрытии задания: "+task.title, date=datetime.datetime.today())
                user_balance.save()

            us_s = Users.objects.get(auth_user=task.exec)
            if us_s.get_notice_status:
                em = settings.EMAIL_HOST_USER
                subject, from_email, to = 'Изменение статуса задания', em, task.exec.email
                text_content = 'Перейдите по ссылке'
                # m = 'https://work-proj.herokuapp.com/verify/' + key
                # print(m)
                html_content = render_to_string('email_other_letter.html', {"title": "Задание закрыто",
                                                                            "text": "Задание успешно закрыто заказчиком. Перейдите по ссылке ниже для получения подробной информации",
                                                                            "url": "http:/www.porabotaem.com/profile/task/detail/" + str(
                                                                                task.id), "url_text": task.title})
                print(html_content)
                # html_content="<a href='%s'>Активировать</a>" % m
                # html_content="<a href='%s'>Активировать</a>" % m
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            admin=Users.objects.get(auth_user__is_superuser=True)
            admin.balance+=price*10/100
            admin.save()

            task_close_count = UserTask.objects.filter(user=task.user).filter(task_status__name='Выполнено').count()
            user_award_count=UserAwards.objects.filter(user=task.user).filter(awards__backend_name='finish_10_task').count()
            award = ""
            if task_close_count == 10:
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='finish_10_task')
                    c_t = 10
            if task_close_count == 50:
                user_award_count = UserAwards.objects.filter(user=task.user).filter(
                    awards__backend_name='finish_50_task').count()
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='finish_50_task')
                    c_t = 50
            if task_close_count == 100:
                user_award_count = UserAwards.objects.filter(user=task.user).filter(
                    awards__backend_name='finish_100_task').count()
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='finish_100_task')
                    c_t = 100
            if award != "":
                user_award = UserAwards(user=task.user, awards=award, date=datetime.datetime.now())
                user_award.save()
                bonus = Bonuses.objects.get(backend_name='reward_exec')
                user=Users.objects.get(auth_user=task.user)
                user.bonus_balance += bonus.count
                user.save()
                send_notice(request,
                            "Вы получили награду за успешно выполненные " + str(c_t) + " заданий и бонус " + str(bonus.count) + " баллов!",
                            "all", user.auth_user.username)

            task_close_count = UserTask.objects.filter(exec=task.exec).filter(task_status__name='Выполнено').count()
            award = ""
            if task_close_count == 5:
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='close_5_task')
                    c_t = 5
            if task_close_count == 10:
                user_award_count = UserAwards.objects.filter(user=task.exec).filter(
                    awards__backend_name='close_10_task').count()
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='close_10_task')
                    c_t = 10
            if task_close_count == 50:
                user_award_count = UserAwards.objects.filter(user=task.exec).filter(
                    awards__backend_name='close_50_task').count()
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='close_50_task')
                    c_t = 50
            if award != "":
                user_award = UserAwards(user=task.exec, awards=award, date=datetime.datetime.now())
                user_award.save()
                bonus = Bonuses.objects.get(backend_name='reward_cust')
                user = Users.objects.get(auth_user=task.exec)
                user.bonus_balance += bonus.count
                user.save()
                send_notice(request,
                            "Вы получили награду за успешно закрытые " + str(c_t) + " заданий и бонус " + str(bonus.count) + " баллов!",
                            "all",user.auth_user.username)

            return HttpResponseRedirect("/profile/task/exec_comment/"+str(task.id)+"/"+str(task.exec.id))
        else:
            return HttpResponseRedirect("/profile/task")
    else:
        return HttpResponseRedirect("/login")


def In_work_task(request):
    work=request.POST.get('message-text')
    task_id=request.POST.get('task-id')
    task=UserTask.objects.get(id=task_id)
    task.comment=work
    task.task_status=UserTaskStatus.objects.get(name='В работе')
    task.save()
    us_s = Users.objects.get(auth_user=task.exec)
    if us_s.get_notice_status:
        em = settings.EMAIL_HOST_USER
        subject, from_email, to = 'Изменение статуса задания', em, task.exec.email
        text_content = 'Перейдите по ссылке'
        # m = 'https://work-proj.herokuapp.com/verify/' + key
        # print(m)
        html_content = render_to_string('email_other_letter.html', {"title": "Возврат в работу",
                                                                    "text": "Задание было возвращено в работу. Перейдите по ссылке ниже для получения подробной информации",
                                                                    "url": "http:/www.porabotaem.com/profile/task/detail/" + str(task.id), "url_text": task.title})
        print(html_content)
        # html_content="<a href='%s'>Активировать</a>" % m
        # html_content="<a href='%s'>Активировать</a>" % m
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    return HttpResponseRedirect("/profile/task/detail/"+task_id)

def Exec_comment(request, task_id, exec_id):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    task_id=int(task_id)
    exec_id=int(exec_id)
    return render(request, 'Profile/Exec_comment.html', locals())

def Save_exec_comment(request):
    task_id=request.POST.get('task_id')
    exec_id=request.POST.get('exec_id')
    text=request.POST.get('comment_text')
    rating_quality=request.POST.get('rating_quality')
    rating_politeness=request.POST.get('rating_politeness')
    rating_punctuality=request.POST.get('rating_punctuality')
    if rating_quality == None:
        rating_quality=0
    if rating_politeness == None:
        rating_politeness=0
    if rating_punctuality == None:
        rating_punctuality=0
    task=UserTask.objects.get(id=task_id)
    u = request.session.get('username')
    customer = AuthUser.objects.get(username=u)
    user=AuthUser.objects.get(id=exec_id)
    user_comment=UserComment(user=user, text=text, task=task, customer=customer, quality=rating_quality, politeness=rating_politeness, punctuality=rating_punctuality, date=datetime.datetime.now())
    user_comment.save()

    cust_comment_count = UserComment.objects.filter(customer=customer).count()
    cust_award_count = UserAwards.objects.filter(user=customer).filter(awards__backend_name='left_10_comments').count()
    award = ""
    if cust_comment_count == 10:
        if cust_award_count == 0:
            award = Awards_model.objects.get(backend_name='left_10_comments')
            c_t = 10
    if cust_comment_count == 20:
        cust_award_count = UserAwards.objects.filter(user=user).filter(
            awards__backend_name='left_20_comments').count()
        if cust_award_count == 0:
            award = Awards_model.objects.get(backend_name='left_20_comments')
            c_t = 20
    if cust_comment_count == 50:
        cust_award_count = UserAwards.objects.filter(user=user).filter(
            awards__backend_name='left_50_comments').count()
        if cust_award_count == 0:
            award = Awards_model.objects.get(backend_name='left_50_comments')
            c_t = 50
    if award != "":
        user_award = UserAwards(user=customer, awards=award, date=datetime.datetime.today())
        user_award.save()
        bonus = Bonuses.objects.get(backend_name='reward_cust')
        customer.bonus_balance += bonus.count
        customer.save()
        send_notice(request,
                    "Вы получили награду за " + str(c_t) + " положительных отзывов и бонус " + str(bonus.count) + " баллов!",
                    "all",customer.username)


    user_comment_count = UserComment.objects.filter(user=user).filter(quality__gte=4).filter(politeness__gte=4).filter(punctuality__gte=4).count()
    user_award_count = UserAwards.objects.filter(user=user).filter(awards__backend_name='positive_comments_10').count()
    award = ""
    if user_comment_count == 10:
        if user_award_count == 0:
            award = Awards_model.objects.get(backend_name='positive_comments_10')
            c_t = 10
    if user_comment_count == 20:
        user_award_count = UserAwards.objects.filter(user=user).filter(awards__backend_name='positive_comments_20').count()
        if user_award_count == 0:
            award = Awards_model.objects.get(backend_name='positive_comments_20')
            c_t = 20
    if user_comment_count == 50:
        user_award_count = UserAwards.objects.filter(user=user).filter(awards__backend_name='positive_comments_50').count()
        if user_award_count == 0:
            award = Awards_model.objects.get(backend_name='positive_comments_50')
            c_t = 50
    if award != "":
        user_award = UserAwards(user=user, awards=award, date=datetime.datetime.now())
        user_award.save()
        bonus = Bonuses.objects.get(backend_name='reward_exec')
        user.bonus_balance += bonus.count
        user.save()
        send_notice(request, "Вы получили награду за " + str(c_t) + " положительных отзывов и бонус " + str(bonus.count) + " баллов!",
                    "all", user.username)


    return HttpResponseRedirect("/profile/task")


def Find(request):
    layout, username, photo, balance, bonus = layout_name(request)
    user = request.session.get('username', 'no')
    contact = layout_contact()
    link = layout_link()
    if (user != 'no'):
        user = AuthUser.objects.all().filter(email=user)[0]
        user_subcategory=UserSubcategories.objects.filter(user=user)
        subcategory=[]
        for i in user_subcategory:
            if i.subcategories not in subcategory:
                subcategory.append(i.subcategories)
        task_count = UserTask.objects.filter(subcategory__in=subcategory).filter(task_status=UserTaskStatus.objects.get(name='В поиске')).count()
        if task_count > 10:
            task=UserTask.objects.filter(subcategory__in=subcategory).filter(task_status=UserTaskStatus.objects.get(name='В поиске'))[0:10]
        else:
            task=UserTask.objects.filter(subcategory__in=subcategory).filter(task_status=UserTaskStatus.objects.get(name='В поиске'))[0:]
        k = 0
        while (task_count > 0):
            k = k + 1
            task_count = task_count - 10
        list_page = []
        page = 1
        if (k > 6):
            for i in range(1, 4):
                list_page.append(i)
            list_page.append('...')
            for i in range(k - 2, k + 1):
                list_page.append(i)
        else:
            for i in range(1, k + 1):
                list_page.append(i)
        pre = 1
        next = page + 1
        # print(task)
        return render(request, 'Profile/Find_task.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Find_page(request, page):
    layout, username, photo, balance, bonus = layout_name(request)
    user = request.session.get('username', 'no')
    contact = layout_contact()
    link = layout_link()
    if (user != 'no'):
        user = AuthUser.objects.all().filter(email=user)[0]
        user_subcategory = UserSubcategories.objects.filter(user=user)
        subcategory = []
        for i in user_subcategory:
            if i.subcategories not in subcategory:
                subcategory.append(i.subcategories)
        page = int(page)
        start = page * 10 - 10
        end = page * 10
        task_count = UserTask.objects.filter(subcategory__in=subcategory).filter(task_status=UserTaskStatus.objects.get(name='В поиске')).count()
        task = UserTask.objects.filter(subcategory__in=subcategory).filter(task_status=UserTaskStatus.objects.get(name='В поиске'))[start:end]
        k = 0
        while (task_count > 0):
            k = k + 1
            task_count = task_count - 10
        Page = []
        if k > 6:
            # записать первые 3
            for i in range(1, 4):
                Page.append(i)
            # записать середину
            if page >= 3 and page <= (k - 2):
                for i in range(page - 1, page + 2):
                    Page.append(i)
            # записать последние 3
            for i in range(k - 2, k + 1):
                Page.append(i)
        else:
            for i in range(1, k + 1):
                Page.append(i)
        # убрать повторения
        Page = list(set(Page))
        print(Page)
        list_page = []
        # добавить '...'
        for i in range(len(Page) - 1):
            list_page.append(Page[i])
            if Page[i + 1] - Page[i] > 1:
                list_page.append('...')
        list_page.append(Page[len(Page) - 1])
        pre = page - 1
        next = page + 1
        return render(request, 'Profile/Find_task.html', locals())
    else:
        return HttpResponseRedirect("/login")