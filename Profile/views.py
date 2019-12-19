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

# Create your views here.
def Profile_settings(request):
    layout, username,photo = layout_name(request)
    if(username != ''):
        email = request.session.get('username', 'no')
        user=Users.objects.all().filter(auth_user__email=email)[0]
        if(user.birthday==None):
            day = ""
            month = ""
            year = ""
        else:
            day=user.birthday.day
            if(day<10):
                day = '0' + str(user.birthday.day)
            month = user.birthday.month
            if(month<10):
                month='0'+str(user.birthday.month)
            year=user.birthday.year
        # print(str(user.birthday.day)+'.'+str(user.birthday.month)+'.'+str(user.birthday.year))
        subcategory=UserSubcategories.objects.all().filter(user__email=email)
        cities = UserCities.objects.all().filter(user__email=email)
        portfolio=UserPortfolio.objects.all().filter(user__email=email)
        return render(request, 'Profile/Profile_settings.html', locals())
    else:
        return HttpResponseRedirect("/login")

def Portfolio_add(request):
    print('portfolio_add')
    if request.method == 'POST':
        doc = request.FILES
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        if (doc):
            for d in doc.getlist('files'):
                user_portfolio=UserPortfolio(user=auth, photo=d)
                user_portfolio.save()
    return HttpResponseRedirect("/profile/settings")


def Delete_portfolio(request):
    if request.method == 'POST':
        id=request.POST.get('delete_id')
        id=id.split(',')
        print(id)
        for el in id:
            if(el != ""):
                user_portfolio=UserPortfolio.objects.get(id=el)
                user_portfolio.delete()
    return HttpResponseRedirect("/profile/settings")

def Save(request):
    print('save')
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        gender=''
        if(request.POST.get('gender') == '1'):
            gender=Gender.objects.all().filter(name="Мужской")[0]
        else:
            gender = Gender.objects.all().filter(name="Женский")[0]
        user.birthday=request.POST.get('birthday')
        user.gender_id=gender
        user.about_me=request.POST.get('about')
        user.phone = request.POST.get('phone')
        user.save()

    return HttpResponseRedirect("/profile/settings")

def Save_photo(request):
    print('save_photo')
    if request.method == 'POST':
        doc = request.FILES
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        if(doc):
            user.photo = doc['files']
        username=request.POST.get('user_name')
        username=username.split(' ')
        if(len(username) == 2):
            user.auth_user.first_name=username[0]
            user.auth_user.last_name=username[1]
        user.auth_user.save()
        user.save()
    return HttpResponseRedirect("/profile/settings")


def Choose_city(request):
    layout, username,photo = layout_name(request)

    regions = Region.objects.all().order_by('name')
    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    user_id = AuthUser.objects.get(username=user).id
    user_cities = UserCities.objects.filter(user_id=user_id)
    list_cities = []
    for i in user_cities:
        list_cities.append(i.city_id)

    if (username != ''):
        return render(request, 'Profile/Choose_city.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Advert_add(request, name):
    print('advert')
    layout, username,photo = layout_name(request)
    if (username != ''):
        subcategory=SubCategory.objects.all().filter(name=name)[0]
        return render(request, 'Profile/Adverts_add.html', locals())
    else:
        return HttpResponseRedirect("/login")

def Advert_save(request):
    print('advert_save')
    if request.method == 'POST':
        doc = request.FILES
        email = request.session.get('username', 'no')
        title=request.POST.get('advert_title')
        price=request.POST.get('advert_price')
        date=datetime.datetime.now().date()
        sub=request.POST.get('advert_category')
        description=request.POST.get('advert_description')
        auth=AuthUser.objects.all().filter(email=email)[0]
        subcategory=SubCategory.objects.all().filter(name=sub)[0]
        if (doc):
            user_advert=UserAdvert(user=auth, subcategory=subcategory, title=title, description=description, photo_main=doc['main_file'], price=price, date=date)
        else:
            user_advert = UserAdvert(user=auth, subcategory=subcategory, title=title, description=description, price=price, date=date)
        user_advert.save()
        if (doc):
            for d in doc.getlist('files'):
                user_advert_photo=UserAdvertPhoto(user=auth, advert=user_advert, photo=d)
                user_advert_photo.save()
    return HttpResponseRedirect("/profile/settings")




def Choose_categ(request):
    layout, username,photo = layout_name(request)

    category=Category.objects.all().order_by('name')
    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    user_id = AuthUser.objects.get(username=user).id
    user_cat=UserSubcategories.objects.filter(user_id=user_id)
    cats=[]
    for i in user_cat:
        cats.append(i.subcategories_id)

    if (username != ''):
        return render(request, 'Profile/Choose_categ.html', locals())
    else:
        return HttpResponseRedirect("/login")


def change_password(request):
    old = request.GET.get('old')
    new1 = request.GET.get('new1')
    new2 = request.GET.get('new2')

    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z]{8,}$')
    db_pass = AuthUser.objects.get(id=user_id).password
    check = check_password(old, db_pass)

    if (check == True):
        if new1 == new2:
            check_sym = bool(pattern_password.match(new1))
            print(check_sym)
            if check_sym == True:
                if check_password(new1, db_pass) == False:
                    new_pass = make_password(new1)
                    set_pass = AuthUser.objects.get(id=user_id)
                    set_pass.password = new_pass
                    set_pass.save()
                    return HttpResponse(json.dumps(True))
                else:
                    return HttpResponse(json.dumps('Новый пароль должен отличаться от старого!'))
            else:
                return HttpResponse(
                    json.dumps(
                        'Пароль должен содержать только латинские буквы, как минимум одну заглавную букву и цифру!'))
        else:
            return HttpResponse(json.dumps('Пароли не совпадают!'))
    else:
        return HttpResponse(json.dumps('Старый пароль неверный'))


def get_new_order(request):
    user = request.session.get('username', 0)
    print(user)
    status = bool(strtobool(request.GET.get('status')))
    print(status)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    set_status = Users.objects.get(auth_user=user_id)
    set_status.get_new_order = status
    set_status.save()
    if status == True:
        return HttpResponse(json.dumps('Теперь на вашу почту будет приходить рассылка заказов'))
    else:
        return HttpResponse(json.dumps('Рассылка заказов более приходить не будет'))


def get_notice_status(request):
    user = request.session.get('username', 0)
    print(user)
    status = bool(strtobool(request.GET.get('status')))
    print(status)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    set_status = Users.objects.get(auth_user=user_id)
    set_status.get_notice_status = status
    set_status.save()
    if status == True:
        return HttpResponse(
            json.dumps('Теперь на вашу почту будут приходить уведомления об изменениях статусов заказов'))
    else:
        return HttpResponse(json.dumps('Уведомления об изменениях статусов заказов более приходить не будут'))


def get_status(request):
    user = request.session.get('username', 0)
    print(user)
    if user == 0:
        return HttpResponse(json.dumps('Ошибка, попробуйте позже'))
    user_id = AuthUser.objects.get(username=user).id
    get_status = Users.objects.get(auth_user=user_id)
    list = []
    list.append(get_status.get_notice_status)
    list.append(get_status.get_new_order)
    print(list)

    return HttpResponse(json.dumps(list))

# def load_photos(request):
#     files=request.GET.get('files')
#     files=request.FILES['newsslide']
#     print(files)
#
#     return HttpResponse(json.dumps('good'))

def profile_set_subcategories(request):
    id=request.GET.get('id')
    status=bool(strtobool(request.GET.get('status')))
    id=str(id).split('_')[2]

    user = request.session.get('username', 0)
    print(user)
    if user != 0:
        us=AuthUser.objects.get(username=user).id
        sub=SubCategory.objects.get(id=id).id
        if status==True:
            UserSubcategories.objects.create(user_id=us,subcategories_id=sub)
        else:
            UserSubcategories.objects.get(user_id=us, subcategories_id=sub).delete()
    return HttpResponse(json.dumps('good'))

def profile_set_cities(request):
    id=request.GET.get('id')
    status=bool(strtobool(request.GET.get('status')))
    id=str(id).split('_')[2]

    user = request.session.get('username', 0)
    print(user)
    if user != 0:
        us=AuthUser.objects.get(username=user).id
        city=City.objects.get(id=id).id
        if status==True:
            UserCities.objects.create(user_id=us,city_id=city)
        else:
            UserCities.objects.get(user_id=us, city_id=city).delete()
    return HttpResponse(json.dumps('good'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

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
        doc = request.FILES
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
        date_=date_.split('/')
        date=date_[2]+'-'+date_[1]+'-'+date_[0]
        pay=1

        auth = AuthUser.objects.all().filter(email=email)[0]
        subcategory = SubCategory.objects.all().filter(id=sub)[0]
        city=City.objects.all().filter(id=city)[0]
        if(gridRadios2 == 'option1'):
            pay=0
        if(gridRadios=='option1'):
            user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description, city=city,
                                 address=address,date=date,pay=pay)
        else:
            user_task = UserTask(user=auth, subcategory=subcategory, title=title, description=description, city=city,
                                 address=address, start_time=start_time,end_time=end_time, date=date, pay=pay)
        user_task.save()
        if (doc):
            for d in doc.getlist('files'):
                tast_photo = TaskPhoto(task=user_task, photo=d)
                tast_photo.save()
    return HttpResponseRedirect("/profile/settings")

def Executor(request):
    email = request.session.get('username', 'no')
    user = Users.objects.all().filter(auth_user__email=email)[0]
    user.type=UserType.objects.all().filter(name="Исполнитель")[0]
    user.save()
    return HttpResponse(json.dumps({'data': 'ok'}))

def Customer(request):
    email = request.session.get('username', 'no')
    user = Users.objects.all().filter(auth_user__email=email)[0]
    user.type=UserType.objects.all().filter(name="Заказчик")[0]
    user.save()
    return HttpResponse(json.dumps({'data': 'ok'}))

def All_ads(request):
    layout, username, photo = layout_name(request)
    if (username != ''):
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        filter=0
        ads_categ=UserSubcategories.objects.all().filter(user=auth)
        ads_count = UserAdvert.objects.filter(user=auth).order_by('-date').count()
        if(ads_count<10):
            ads=UserAdvert.objects.all().filter(user=auth).order_by('-date')[0:]
        else:
            ads = UserAdvert.objects.all().filter(user=auth).order_by('-date')[0:10]
        k = 0
        while (ads_count > 0):
            k = k + 1
            ads_count = ads_count - 10
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
        return render(request, 'Profile/All_ads.html', locals())
    else:
        return HttpResponseRedirect("/login")

def All_ads_page(request,page):
    layout, username, photo = layout_name(request)
    if (username != ''):
        filter = 0
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        filter = 0
        ads_categ = UserSubcategories.objects.all().filter(user=auth)
        ads_count = UserAdvert.objects.filter(user=auth).order_by('-date').count()
        page = int(page)
        start = page * 10 - 10
        end = page * 10
        ads=UserAdvert.objects.all().filter(user=auth).order_by('-date')[start:end]
        k = 0
        while (ads_count > 0):
            k = k + 1
            ads_count = ads_count - 10
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
        return render(request, 'Profile/All_ads.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Advert_filter(request, filter):
    layout, username, photo = layout_name(request)
    filter = str(filter)
    if (username != ''):
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        ads_categ=UserSubcategories.objects.all().filter(user=auth)
        ads_count = UserAdvert.objects.filter(user=auth).filter(subcategory__name=filter).order_by('-date').count()
        if (ads_count < 10):
            ads=UserAdvert.objects.all().filter(user=auth).filter(subcategory__name=filter).order_by('-date')[0:]
        else:
            ads=UserAdvert.objects.all().filter(user=auth).filter(subcategory__name=filter).order_by('-date')[0:10]
        k = 0
        while (ads_count > 0):
            k = k + 1
            ads_count = ads_count - 10
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
        return render(request, 'Profile/All_ads.html', locals())
    else:
        return HttpResponseRedirect("/login")

def Advert_filter_page(request, filter, page):
    layout, username, photo = layout_name(request)
    filter = str(filter)
    if (username != ''):
        filter = 0
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        ads_categ = UserSubcategories.objects.all().filter(user=auth)
        ads_count = UserAdvert.objects.filter(user=auth).filter(subcategory__name=filter).order_by('-date').count()
        page = int(page)
        start = page * 10 - 10
        end = page * 10
        ads = UserAdvert.objects.all().filter(user=auth).filter(subcategory__name=filter).order_by('-date')[start:end]
        k = 0
        while (ads_count > 0):
            k = k + 1
            ads_count = ads_count - 10
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
        return render(request, 'Profile/All_ads.html', locals())
    else:
        return HttpResponseRedirect("/login")

# def Ads_details(request,id):
#     layout, username, photo = layout_name(request)
#     return render(request, 'Profile/Advert_change.html', locals())

def Customer_my_tasks(request):
    layout, username, photo = layout_name(request)
    if username=='':
        return HttpResponseRedirect("/login")
    else:
        email = request.session.get('username', 'no')
        if (Users.objects.all().filter(auth_user__email=email)[0].type.name == 'Заказчик'):
            us = request.session.get('username')
            user=AuthUser.objects.get(username=us).id
            filter=0
            task_count = UserTask.objects.filter(user_id=user).order_by('-date').count()
            if (task_count < 10):
                task=UserTask.objects.filter(user_id=user).order_by('-date')[0:]
            else:
                task=UserTask.objects.filter(user_id=user).order_by('-date')[0:10]
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

        else:
            return HttpResponseRedirect("/profile/settings")
    return render(request, 'Profile/My_tasks_customer.html', locals())

def Customer_tasks_page(request,page):
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

def My_tasks_customer_filter(request,filter):
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
            task_count = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date').count()
            if (task_count < 10):
                # task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[0:]
                task = UserTask.objects.filter(user_id=user).order_by('-date')[0:]
            else:
                # task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[0:10]
                task = UserTask.objects.filter(user_id=user).order_by('-date')[0:10]
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

def My_tasks_customer_page_filter(request,filter,page):
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
            task = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date')[start:end]
            task_count = UserTask.objects.filter(user_id=user).filter(subcategory__id=cat).order_by('-date').count()
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



def Executor_my_tasks(request):
    layout, username, photo = layout_name(request)


    return render(request, 'Profile/My_tasks_executor.html', locals())

def Fav_executor(request):
    layout, username, photo = layout_name(request)
    return render(request, 'Profile/Fav_executor.html', locals())

def Offer(request):
    layout, username, photo = layout_name(request)
    return render(request, 'Profile/Offers.html', locals())

# def check_user(request,type_user):
#     #заказчик - true, исполнитель - false 'Заказчик'
#     user = request.session.get('username', 0)
#     if user==0:
#         return HttpResponseRedirect("/login")
#     # if Users.objects.get(auth_user__email=user).type.name != type_user:
#     #     return HttpResponseRedirect("/profile/settings")
#     return AuthUser.objects.get(username=user).id

def Advert_detail(request,id):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    else:
        user_id=AuthUser.objects.get(username=user).id
        user_type=Users.objects.get(auth_user=user_id).type.name

    # city, regs, regions = layout_regions_cities(request)
    id=int(id)
    # advert = UserAdvert.objects.filter(id=id)[0]
    advert = UserAdvert.objects.get(id=id)
    advert_photo=UserAdvertPhoto.objects.filter(advert_id=id)
    sub = SubCategory.objects.filter(name__icontains = advert.subcategory.name)
    # print(sub)
    return render(request, 'Profile/Advert_detail.html', locals())



def Adverts_change(request,id):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    else:
        user_id = AuthUser.objects.get(username=user).id
        user_type = Users.objects.get(auth_user=user_id).type.name

    # check_user(request, 'Заказчик')
    # city, regs, regions = layout_regions_cities(request)
    id=int(id)
    advert = UserAdvert.objects.filter(id=id)[0]
    advert_photo=UserAdvertPhoto.objects.filter(advert_id=id)
    sub = SubCategory.objects.filter(name__icontains = advert.subcategory.name)
    # print('start')
    # print(check_user(request,'Заказчик'))
    # print(sub)
    return render(request, 'Profile/Advert_change.html', locals())


def user_delete_ads(request):
    id = int(request.GET.get('id'))

    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponse(json.dumps(False))
    else:
        user_id = AuthUser.objects.get(username=user).id
    advert=UserAdvert.objects.get(id=id)

    if advert.user_id ==user_id:
        photos=UserAdvertPhoto.objects.filter(id=advert.id)
        for i in photos:
            i.delete()
        advert.delete()
    return HttpResponse(json.dumps(True))