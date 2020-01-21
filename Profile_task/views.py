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
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        photo=Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout,username,photo



def Profile_tasks(request):
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
            for i in user_task:
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
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    layout, username,photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
        # subcategory_list = []
        # for s in subcategory:
        #     subcategory_list.append(s.id)
        #     subcategory_list.append(s.name)
        price=subcategory.price
        return HttpResponse(json.dumps({'data': price}))
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
        price = request.POST.get('input_price')
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
        if (gridRadios2 == 'option1'):
            pay = 0
        if (gridRadios == 'option1'):
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     photo_main=doc['file_main'], task_status=status, date_add=datetime.datetime.now(),
                                     rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price, task_status=status,
                                     date_add=datetime.datetime.now(), rezult_text="")
        else:
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, photo_main=doc['file_main'], task_status=status,
                                     date_add=datetime.datetime.now(), rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, task_status=status, date_add=datetime.datetime.now(),
                                     rezult_text="")
        user_task.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
    return HttpResponseRedirect("/profile/task")


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
        exec=AuthUser.objects.get(id=advert.user.id)
        doc = request.FILES
        city = City.objects.all().filter(id=city)[0]
        if (gridRadios2 == 'option1'):
            pay = 0
        if (gridRadios == 'option1'):
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     photo_main=doc['file_main'], date_add=datetime.datetime.now(),
                                     offer=offer, exec=exec, rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, date=date, pay=pay, price=price,
                                     date_add=datetime.datetime.now(), offer=offer, exec=exec, rezult_text="")
        else:
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, photo_main=doc['file_main'],
                                     date_add=datetime.datetime.now(), offer=offer, exec=exec, rezult_text="")
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, date_add=datetime.datetime.now(),
                                     offer=offer, exec=exec, rezult_text="")
        user_task.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
        advert.count_offer=advert.count_offer+1
        advert.save()
    return HttpResponseRedirect("/profile/task")


def Profile_task_detail(request,id):
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
    id=int(request.GET.get('id'))
    description=request.GET.get('description')
    sum=int(request.GET.get('sum'))
    if username == '':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        print(email)
        auth=AuthUser.objects.get(email=email)
        print(auth)
        task=UserTask.objects.get(id=id)
        task_bet=UserTaskBet(user=auth, task=task, description=description, price=sum, date=datetime.datetime.now())
        task_bet.save()
        return HttpResponse(json.dumps({'data': 'ok'}))


def Set_exec(request):
    layout, username, photo = layout_name(request)
    id = int(request.GET.get('id'))
    user_id = int(request.GET.get('user_id'))
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
        return HttpResponse(json.dumps({'data': 'ok'}))


def Executor_my_tasks_filter_cat(request,filter_cat):
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    layout, username, photo = layout_name(request)
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
    return HttpResponseRedirect("/profile/task")


def Close_task(request, id):
    layout, username, photo = layout_name(request)
    if (username != ''):
        email = request.session.get('username', 'no')
        id=int(id)
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            task=UserTask.objects.get(id=id)
            task.task_status=UserTaskStatus.objects.get(name='Выполнено')
            task.save()
            return HttpResponseRedirect("/profile/task")
        else:
            return HttpResponseRedirect("/profile/task")
    else:
        return HttpResponseRedirect("/login")
