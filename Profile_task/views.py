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
            all_user_task = task = UserTask.objects.filter(user_id=user)
            task_count = UserTask.objects.filter(user_id=user).order_by('-date').count()
            if (task_count < 10):
                task=UserTask.objects.filter(user_id=user).order_by('-date')[0:]
            else:
                task=UserTask.objects.filter(user_id=user).order_by('-date')[0:10]
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
            user_tasks = UserTask.objects.filter(exec_id=user)
            list_cat = []
            for i in user_tasks:
                sub = i.subcategory.name
                if sub not in list_cat:
                    list_cat.append(sub)
            list_stat = []
            for i in user_tasks:
                sub = i.task_status.name
                if sub not in list_stat:
                    list_stat.append(sub)
            list_cat.sort()
            list_stat.sort()
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
            task = UserTask.objects.filter(user_id=user).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(user_id=user).order_by('-date').count()
            cats = []
            for i in task:
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
            all_user_task=task = UserTask.objects.filter(user_id=user)
            task_count = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date').count()
            if (task_count < 10):
                task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[0:]
            else:
                task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[0:10]
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
            all_user_task = task = UserTask.objects.filter(user_id=user)
            task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date').count()
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
    print('start')
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

def SubcategoryFind(request):
    try:
        cat = request.GET.get("id")
        subcategory=SubCategory.objects.all().filter(category__id=cat)
        subcategory_list = []
        for s in subcategory:
            subcategory_list.append(s.id)
            subcategory_list.append(s.name)
        return HttpResponse(json.dumps({'data': subcategory_list}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))

def Save_task(request):
    print('task_save')
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        sub=request.POST.get('subcategory')
        title = request.POST.get('task_title')
        description=request.POST.get('description')
        city=request.POST.get('city')
        address=request.POST.get('address')
        date_=request.POST.get('date')
        gridRadios=request.POST.get('gridRadios')
        start_time=request.POST.get('start_time')
        end_time=request.POST.get('end_time')
        gridRadios2=request.POST.get('gridRadios2')
        price=request.POST.get('input_price')
        print(date_)
        date_=date_.split('/')
        date=date_[2]+'-'+date_[0]+'-'+date_[1]
        print(date)
        pay=1

        auth = AuthUser.objects.all().filter(email=email)[0]
        subcategory = SubCategory.objects.all().filter(id=sub)[0]
        status=UserTaskStatus.objects.get(name='В поиске')
        doc = request.FILES
        city=City.objects.all().filter(id=city)[0]
        if(gridRadios2 == 'option1'):
            pay=0
        if(gridRadios=='option1'):
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city,address=address,date=date,pay=pay, price=price,
                                     photo_main=doc['file_main'], task_status=status, date_add=datetime.datetime.now())
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city,address=address, date=date, pay=pay, price=price, task_status=status,
                                     date_add=datetime.datetime.now())
        else:
            if (doc):
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city,address=address, start_time=start_time,end_time=end_time, date=date,
                                     pay=pay, price=price,  photo_main=doc['file_main'], task_status=status,
                                     date_add=datetime.datetime.now())
            else:
                user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description,
                                     city=city, address=address, start_time=start_time, end_time=end_time, date=date,
                                     pay=pay, price=price, task_status=status, date_add=datetime.datetime.now())
        user_task.save()
        docs = request.FILES
        if (docs):
            for d in docs.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
    return HttpResponseRedirect("/profile/settings")