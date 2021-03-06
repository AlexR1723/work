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


def send_notice(request, text, is_executor, user_id):
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
        user = Users.objects.get(auth_user=auth)
        user_advert_count=UserAdvert.objects.filter(user=auth).count()
        user_advert_sub=UserAdvert.objects.filter(user=auth)
        user_advert_sub_list=[]
        for s in user_advert_sub:
            if s.subcategory.id not in user_advert_sub_list:
                user_advert_sub_list.append(s.subcategory.id)

        user_bonuses_count = UserBonuses.objects.filter(bonus__backend_name='create_2_ad_2_sub').count()
        bonus = ""
        c_ad=0
        c_sub=0
        if user_bonuses_count == 0:
            if user_advert_count == 2 and len(user_advert_sub_list) == 2:
                bonus = Bonuses.objects.get(backend_name='create_2_ad_2_sub')
                c_ad=2
                c_sub=2
        else:
            user_bonuses_count = UserBonuses.objects.filter(bonus__backend_name='create_5_ad_3_sub').count()
            if user_bonuses_count == 0:
                if user_advert_count == 5 and len(user_advert_sub_list) == 3:
                    bonus = Bonuses.objects.get(backend_name='create_5_ad_3_sub')
                    c_ad=5
                    c_sub=3
            else:
                user_bonuses_count = UserBonuses.objects.filter(bonus__backend_name='create_10_ad_5_sub').count()
                if user_bonuses_count == 0:
                    if user_advert_count == 10 and len(user_advert_sub_list) == 5:
                        bonus = Bonuses.objects.get(backend_name='create_10_ad_5_sub')
                    c_ad=10
                    c_sub=5
            if bonus != "":
                user_bonuses = UserBonuses(bonus=bonus, user=auth)
                user_bonuses.save()
                user.bonus_balance += bonus.count
                user.save()
                send_notice(request, "Вы получили бонус "+str(bonus.count)+" баллов за создание "+str(c_ad)+" объявлений в "+str(c_sub)+" подкатегориях!", "all")

        user_advert_count = UserAdvert.objects.filter(user=auth).count()
        user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='posted_5_ads').count()
        award = ""
        c_p=0
        if user_advert_count == 5:
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='posted_5_ads')
                c_p=5
        if user_advert_count == 10:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='posted_10_ads').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='posted_10_ads')
                c_p=10
        if user_advert_count == 20:
            user_award_count = UserAwards.objects.filter(user=auth).filter(awards__backend_name='posted_20_ads').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='posted_20_ads')
                c_p=20
        if award != "":
            user_award = UserAwards(user=auth, awards=award, date=datetime.datetime.now())
            user_award.save()
            bonus = Bonuses.objects.get(backend_name='reward_exec')
            user.bonus_balance += bonus.count
            user.save()
            send_notice(request, "Вы получили награду за публикацию "+str(c_p)+" объявлений и бонус "+str(bonus.count)+" баллов!", "all")
    return HttpResponseRedirect("/profile/service/advert_add/" + str(user_advert.id))
    # return HttpResponseRedirect("/profile/settings")


def All_ads(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
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
    contact = layout_contact()
    link = layout_link()
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
    contact = layout_contact()
    link = layout_link()
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
    contact = layout_contact()
    link = layout_link()
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