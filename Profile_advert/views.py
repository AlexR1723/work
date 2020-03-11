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
    return HttpResponseRedirect("/profile/service/advert_add/" + str(user_advert.id))
    # return HttpResponseRedirect("/profile/settings")


def All_ads(request):
    layout, username, photo, balance, bonus = layout_name(request)
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
    layout, username, photo, balance, bonus = layout_name(request)
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
    layout, username, photo, balance, bonus = layout_name(request)
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
    layout, username, photo, balance, bonus = layout_name(request)
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

def Advert_detail(request,id):
    layout, username, photo, balance, bonus = layout_name(request)
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
    layout, username, photo, balance, bonus = layout_name(request)
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
        advert.delete()
        # photos=UserAdvertPhoto.objects.filter(id=advert.id)
        # for i in photos:
        #     i.delete()

    return HttpResponse(json.dumps(True))

def Edit_advert_save(request):
    print('edit_advert_save')
    if request.method == 'POST':
        id=request.POST.get('adv_id')
        id_photo=request.POST.get('del_list')
        id_photo=id_photo.split(',')
        print(id_photo)
        for el in id_photo:
            if(el != ""):
                user_advert_photo = UserAdvertPhoto.objects.get(id=el)
                user_advert_photo.delete()
        email = request.session.get('username', 'no')
        auth = AuthUser.objects.all().filter(email=email)[0]
        user_advert=UserAdvert.objects.get(id=id)
        title=request.POST.get('adv_title')
        price=request.POST.get('adv_price')
        description=request.POST.get('adv_desription')
        user_advert.title=title
        user_advert.price=price
        user_advert.description=description
        main_photo = request.FILES
        if (main_photo):
            user_advert.photo_main = main_photo['files_main']
        user_advert.save()
        doc = request.FILES
        if (doc):
            for d in doc.getlist('files'):
                user_advert_photo = UserAdvertPhoto(advert=user_advert, user=auth, photo=d)
                user_advert_photo.save()
    return HttpResponseRedirect("/profile/advert")