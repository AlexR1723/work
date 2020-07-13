from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, re
from .models import *
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from distutils.util import strtobool
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
import datetime
import calendar

import os

list_page = []
ads_count = 0
message = 0


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


def send_notice(request, text, is_executor, user_id=False):
    # all, exec, cust
    if not user_id:
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


# Create your views here.
def Profile_settings(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if (username != ''):
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        if (user.birthday == None):
            day = ""
            month = ""
            year = ""
        else:
            day = user.birthday.day
            if (day < 10):
                day = '0' + str(user.birthday.day)
            month = user.birthday.month
            if (month < 10):
                month = '0' + str(user.birthday.month)
            year = user.birthday.year
        # print(str(user.birthday.day)+'.'+str(user.birthday.month)+'.'+str(user.birthday.year))
        city = City.objects.all().order_by('name')
        subcategory = UserSubcategories.objects.all().filter(user__email=email)
        cities = UserCities.objects.all().filter(user__email=email)
        portfolio = UserPortfolio.objects.all().filter(user__email=email)
        global message
        alert = message
        print(message)
        all_task = UserComment.objects.filter(user__email=email).count()
        successful_task = UserComment.objects.filter(user__email=email).filter(quality__gte=4).filter(
            politeness__gte=4).filter(punctuality__gte=4).count()
        com_percent = 0
        if all_task > 0:
            com_percent = int((successful_task * 100) / all_task)
        balance_list = UserBalance.objects.filter(user=user.auth_user).order_by('-date')
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
                portfolio = UserPortfolio.objects.filter(user=auth)
                if (portfolio.count() < 10):
                    if (d.size <= 31457280):
                        user_portfolio = UserPortfolio(user=auth, photo=d)
                        user_portfolio.save()
                    else:
                        global message
                        message = 1
    return HttpResponseRedirect("/profile/settings")


def Delete_portfolio(request):
    if request.method == 'POST':
        id = request.POST.get('delete_id')
        id = id.split(',')
        print(id)
        for el in id:
            if (el != ""):
                user_portfolio = UserPortfolio.objects.get(id=el)
                user_portfolio.delete()
    return HttpResponseRedirect("/profile/settings")


def Save(request):
    print('save')
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        gender = ''
        if (request.POST.get('gender') == '1'):
            gender = Gender.objects.all().filter(name="Мужской")[0]
        else:
            gender = Gender.objects.all().filter(name="Женский")[0]
        city_id = int(request.POST.get('city'))
        city = City.objects.get(id=city_id)
        birthday = request.POST.get('birthday')
        birthday = birthday.split('/')
        user.birthday = birthday[2] + '-' + birthday[0] + '-' + birthday[1]
        user.gender_id = gender
        user.city = city
        user.about_me = request.POST.get('about')
        user.phone = request.POST.get('phone')
        user.save()
        auth = AuthUser.objects.get(email=email)
        bonus = Bonuses.objects.get(backend_name='profile_100')
        user_bonus_count = UserBonuses.objects.filter(user__email=email).filter(
            bonus__backend_name='profile_100').count()
        if user_bonus_count == 0:
            sub = UserSubcategories.objects.filter(user=auth).count()
            if user.birthday != None and user.birthday != "" and user.phone != None and user.phone != "" and user.about_me != None and user.about_me != "" and sub > 0:
                user_bonus = UserBonuses(user=auth, bonus=bonus)
                user_bonus.save()
                user.bonus_balance += bonus.count
                user.save()
                send_notice(request, "Вы получили бонус " + str(bonus.count) + " баллов за полное заполнение профиля!",
                            "all")

        user_award_count = UserAwards.objects.filter(user__email=email).filter(
            awards__backend_name='profile_100').count()
        if user_award_count == 0:
            if user.birthday != None and user.birthday != "" and user.phone != None and user.phone != "" and user.about_me != None and user.about_me != "":
                award = Awards_model.objects.get(backend_name='profile_100')
                user_award = UserAwards(user=auth, awards=award, date=datetime.datetime.now())
                user_award.save()
                send_notice(request, "Вы получили награду за полное заполнение профиля!", "all")
    return HttpResponseRedirect("/profile/settings")


def Save_photo(request):
    print('save_photo')
    if request.method == 'POST':
        doc = request.FILES
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        if (doc):
            user.photo = doc['files']
        # username = request.POST.get('user_name')
        # username = username.split(' ')
        # if (len(username) == 2):
        #     user.auth_user.first_name = username[0]
        #     user.auth_user.last_name = username[1]
        # user.auth_user.save()
        user.save()
    return HttpResponseRedirect("/profile/settings")


def Choose_city(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    regions = Region.objects.all().order_by('name')
    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    user_id = AuthUser.objects.get(username=user).id
    user_cities = UserCities.objects.filter(user_id=user_id)
    list_cities = []
    for i in user_cities:
        list_cities.append(i.city_id)

    user_regions = UserCities.objects.filter(user_id=user_id)
    list_regions = []
    for i in regions:
        user_cities_reg = UserCities.objects.filter(user_id=user_id).filter(city__region=i)
        cities_reg = City.objects.filter(region=i)
        cities_count = cities_reg.count()
        for j in user_cities:
            if j.city in cities_reg:
                list_regions.append(i.id)
                break
    print(list_regions)

    if (username != ''):
        return render(request, 'Profile/Choose_city.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Advert_add(request, name):
    print('advert')
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    if (username != ''):
        subcategory = SubCategory.objects.all().filter(name=name)[0]
        return render(request, 'Profile/Adverts_add.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Choose_categ(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    category = Category.objects.all().order_by('name')
    user = request.session.get('username', 0)
    if user == 0:
        return HttpResponseRedirect("/login")
    user_id = AuthUser.objects.get(username=user).id
    user_cat = UserSubcategories.objects.filter(user_id=user_id)
    cats = []
    for i in user_cat:
        cats.append(i.subcategories_id)

    list_category = []
    for i in category:
        user_sub_cater = UserSubcategories.objects.filter(user_id=user_id).filter(subcategories__category=i)
        sub_categ = SubCategory.objects.filter(category=i)
        for j in user_cat:
            if j.subcategories in sub_categ:
                list_category.append(i.id)
                break
    print(list_category)

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
    print('set_sub')
    id = request.GET.get('id')
    status = bool(strtobool(request.GET.get('status')))
    id = str(id).split('_')[2]

    user = request.session.get('username', 0)
    print(user)
    if user != 0:
        us = AuthUser.objects.get(username=user).id
        sub = SubCategory.objects.get(id=id).id
        if status == True:
            UserSubcategories.objects.create(user_id=us, subcategories_id=sub)
        else:
            UserSubcategories.objects.get(user_id=us, subcategories_id=sub).delete()
        user_sub = UserSubcategories.objects.filter(user_id=us)
        user_categ = []
        for u in user_sub:
            if u.subcategories.category.id not in user_categ:
                user_categ.append(u.subcategories.category.id)
        print(len(user_categ))
        user_award_count = UserAwards.objects.filter(user__id=us).filter(awards__backend_name='exec_5_categ').count()
        print(user_award_count)
        award = ""
        if len(user_categ) == 5:
            print('first')
            if user_award_count == 0:
                print('second')
                award = Awards_model.objects.get(backend_name='exec_5_categ')
                print(award)
                c_t = 5
                print(5)
        if len(user_categ) == 10:
            user_award_count = UserAwards.objects.filter(user_id=us).filter(
                awards__backend_name='exec_10_categ').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='exec_10_categ')
                c_t = 10
                print(10)
        if len(user_categ) == 20:
            user_award_count = UserAwards.objects.filter(user_id=us).filter(
                awards__backend_name='exec_20_categ').count()
            if user_award_count == 0:
                award = Awards_model.objects.get(backend_name='exec_20_categ')
                c_t = 20
                print(20)
        if award != "":
            user_award = UserAwards(user_id=us, awards=award, date=datetime.datetime.now())
            user_award.save()

            bonus = Bonuses.objects.get(backend_name='reward_exec')
            user = Users.objects.get(auth_user_id=us)
            user.bonus_balance += bonus.count
            user.save()
            send_notice(request,
                        "Вы исполнитель в " + str(c_t) + " категориях и получили бонус " + str(
                            bonus.count) + " баллов!",
                        "all")
    return HttpResponse(json.dumps('good'))


def profile_set_cities(request):
    id = request.GET.get('id')
    status = bool(strtobool(request.GET.get('status')))
    id = str(id).split('_')[2]
    print(id)

    user = request.session.get('username', 0)
    print(user)
    if user != 0:
        us = AuthUser.objects.get(username=user).id
        city = City.objects.get(id=id).id
        if status == True:
            UserCities.objects.create(user_id=us, city_id=city)
        else:
            UserCities.objects.get(user_id=us, city_id=city).delete()
    return HttpResponse(json.dumps('good'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def Executor(request):
    email = request.session.get('username', 'no')
    user = Users.objects.all().filter(auth_user__email=email)[0]
    user.type = UserType.objects.all().filter(name="Исполнитель")[0]
    user.save()
    return HttpResponse(json.dumps({'data': 'ok'}))


def Customer(request):
    email = request.session.get('username', 'no')
    user = Users.objects.all().filter(auth_user__email=email)[0]
    user.type = UserType.objects.all().filter(name="Заказчик")[0]
    user.save()
    return HttpResponse(json.dumps({'data': 'ok'}))


def Fav_executor(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Profile/Fav_executor.html', locals())


def Profile_page(request, id):
    id = int(id)
    layout, username, photo, balance, bonus = layout_name(request)
    user = request.session.get('username', 'no')
    contact = layout_contact()
    link = layout_link()
    if (user != 'no'):
        auth_user = AuthUser.objects.get(id=id)
        user = Users.objects.get(auth_user=auth_user)
        user_city = UserCities.objects.filter(user=auth_user)
        user_sub = UserSubcategories.objects.filter(user=auth_user)
        portfolio = UserPortfolio.objects.filter(user=auth_user)
        # посчитать процент положительных отзывов
        user_comment = UserComment.objects.filter(user=auth_user).order_by('-date')
        successful_task = UserComment.objects.filter(user=auth_user).filter(quality__gte=4).filter(
            politeness__gte=4).filter(punctuality__gte=4).count()
        quality_suc = UserComment.objects.filter(user=auth_user).filter(quality__gte=4).count()
        politeness_suc = UserComment.objects.filter(user=auth_user).filter(politeness__gte=4).count()
        punctuality_suc = UserComment.objects.filter(user=auth_user).filter(punctuality__gte=4).count()
        all_task = user_comment.count()
        com_percent = 0
        quality_percent = 0
        politeness_persent = 0
        punctuality_persent = 0
        if all_task > 0:
            com_percent = int((successful_task * 100) / all_task)
            quality_percent = int((quality_suc * 100) / all_task)
            politeness_persent = int((politeness_suc * 100) / all_task)
            punctuality_persent = int((punctuality_suc * 100) / all_task)

        if (user.verify_passport == True):
            advert_count = UserAdvert.objects.filter(user=auth_user).count()
            if (advert_count > 10):
                advert = UserAdvert.objects.filter(user=auth_user).order_by('-id')[:10]
            else:
                advert = UserAdvert.objects.filter(user=auth_user).order_by('-id')
            task_close = UserTask.objects.filter(exec=auth_user)
            sub_task_close = []
            sub_task_list = ""
            for t in task_close:
                if t.subcategory.name not in sub_task_close:
                    sub_task_close.append(t.subcategory.name)
                    sub_task_list = sub_task_list + t.subcategory.name + "\n"
            advert = UserAdvert.objects.filter(user=auth_user)
            sub_advert = []
            sub_advert_list = ""
            for a in advert:
                if a.subcategory.name not in advert:
                    sub_advert.append(a.subcategory.name)
                    sub_advert_list = sub_advert_list + a.subcategory.name + '\n'
            return render(request, 'Profile/Profile_verified.html', locals())
        else:
            return render(request, 'Profile/Profile_unverified.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Profile_adverts(request, id):
    id = int(id)
    layout, username, photo, balance, bonus = layout_name(request)
    user = request.session.get('username', 'no')
    contact = layout_contact()
    link = layout_link()
    if (user != 'no'):
        auth_user = AuthUser.objects.get(id=id)
        user = Users.objects.get(auth_user=auth_user)
        advert = UserAdvert.objects.filter(user=auth_user)
        # user_city = UserCities.objects.filter(user=auth_user)
        # user_sub = UserSubcategories.objects.filter(user=auth_user)
        # portfolio = UserPortfolio.objects.filter(user=auth_user)
        # # посчитать процент положительных отзывов
        # user_comment = UserComment.objects.filter(user=auth_user).order_by('-date')
        # successful_task = UserComment.objects.filter(user=auth_user).filter(quality__gte=4).filter(
        #     politeness__gte=4).filter(punctuality__gte=4).count()
        # quality_suc = UserComment.objects.filter(user=auth_user).filter(quality__gte=4).count()
        # politeness_suc = UserComment.objects.filter(user=auth_user).filter(politeness__gte=4).count()
        # punctuality_suc = UserComment.objects.filter(user=auth_user).filter(punctuality__gte=4).count()
        # all_task = user_comment.count()
        # com_percent = 0
        # quality_percent = 0
        # politeness_persent = 0
        # punctuality_persent = 0
        # if all_task > 0:
        #     com_percent = int((successful_task * 100) / all_task)
        #     quality_percent = int((quality_suc * 100) / all_task)
        #     politeness_persent = int((politeness_suc * 100) / all_task)
        #     punctuality_persent = int((punctuality_suc * 100) / all_task)
        return render(request, 'Profile/Advert_profile.html', locals())
    else:
        return HttpResponseRedirect("/login")


@login_required()
def Awards_fun(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    user = request.session.get('username')
    if user:
        user = AuthUser.objects.get(username=user).id
        awards = Awards_model.objects.all().order_by('name')
        user_list = UserAwards.objects.filter(user_id=user).values_list('awards_id', 'date')
        user_list = dict(user_list)
    return render(request, 'Profile/Awards.html', locals())


@login_required()
def Number_verification(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    user = request.session.get('username')
    if user:
        user = AuthUser.objects.get(username=user).id
        phonenumber = Users.objects.get(auth_user_id=user).phone
    return render(request, 'Profile/Number_verification.html', locals())


@login_required()
def verify_number(request):
    phone = '+' + str(request.GET.get('phone')).replace(' ', '')
    # phone1=phone[1:]
    # print(phone +' - '+ str(len(phone)))
    print(phone)

    if (phone.startswith('+7') and len(phone) != 12) or (phone.startswith('+38') and len(phone) != 13) or len(
            phone) < 12 or len(phone) > 13:
        return HttpResponse(json.dumps([False, 'Номер введен некоректно!']))

    user = request.session.get('username')
    if user:
        user = AuthUser.objects.get(username=user)

        phonenumber = Users.objects.get(auth_user_id=user.id)
        if phone != phonenumber.phone:
            phonenumber.phone = phone
            phonenumber.save()

        id = user.id
        name = user.first_name
        surename = user.last_name
        # print(user.email)

        subj = 'Запрос на верификацию номера телефона'
        text = 'Данные пользователя: \n\r id: ' + str(
            id) + '\n\r Имя: ' + name + '\n\r Фамилия: ' + surename + '\n\r Номер телефона: ' + phone

        message = send_mail(subj, text, 'romanenko.anastasiya1998@yandex.ua', [user.email])
        # message=True
        if message:
            s = Users.objects.get(auth_user_id=user.id)
            s.verify_date = datetime.datetime.today()
            s.save()
            sn = send_notice(request, 'Ваш номер отправлен на верификацию!', 'all')
            return HttpResponse(json.dumps([True, 'Запрос на верификацию номера отправлен.']))
        else:
            return HttpResponse(json.dumps([False, 'Не удалось отправить запрос на верификацию номера.']))


@login_required()
def Passport_verification(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()

    return render(request, 'Profile/Passport_verification.html', locals())


@login_required()
def verify_passport(request):
    print('verify-passport')
    if request.method == 'POST':
        doc = request.FILES
        passport = str(request.POST.get('series')).replace(' ', '')
        # phone1=phone[1:]
        # print(phone +' - '+ str(len(phone)))
        # print(phone)

        # if (len(passport))==0:
        #     return HttpResponse(json.dumps([False, 'Заполните поля!']))

        user = request.session.get('username')
        if user:
            user = AuthUser.objects.get(username=user)
            if doc:
                user1 = Users.objects.get(auth_user_id=user.id)
                user1.passport_num_ser = passport
                user1.passport_photo = doc['files']
                # user1.save()
                user_bonus_count = UserBonuses.objects.filter(user=user).filter(
                    bonus__backend_name='verify_passport').count()
                if user_bonus_count == 0:
                    bonus = Bonuses.objects.get(backend_name='verify_passport')
                    user_bonus = UserBonuses(user=user, bonus=bonus)
                    user_bonus.save()
                    user1.bonus_balance += bonus.count
                    send_notice(request, "Вы получили бонус " + str(bonus.count) + " баллов за верификацию паспорта!",
                                "all")
                user1.save()
                user_award_count = UserAwards.objects.filter(user=user).filter(
                    awards__backend_name='passport_verify').count()
                if user_award_count == 0:
                    award = Awards_model.objects.get(backend_name='passport_verify')
                    user_award = UserAwards(user=user, awards=award, date=datetime.datetime.now())
                    user_award.save()
                    send_notice(request, "Вы получили награду за верификацию паспорта!", "all")

            id = user.id
            name = user.first_name
            surename = user.last_name
            photo = user1.passport_photo.url
            passport = user1.passport_num_ser
            print(photo)
            print(user.email)

            # subj = 'Запрос на верификацию паспорта'
            # text = 'Данные пользователя: \n\r id: ' + str(
            #     id) + '\n\r Имя: ' + name + '\n\r Фамилия: ' + surename + '\n\r Серия паспорта: ' + passport
            #
            # message = send_mail(subj, text, 'romanenko.anastasiya1998@yandex.ua', [user.email])
            # # message=True
            # if message:
            #     s = Users.objects.get(auth_user_id=user.id)
            #     s.verify_date = datetime.datetime.today()
            #     s.save()
            #     sn = send_notice(request, 'Ваш паспорт отправлен на верификацию. Это может занять несколько дней.', 'all')
            #     return HttpResponse(json.dumps([True, 'Запрос на верификацию паспорта отправлен.']))
            # else:
            #     return HttpResponse(json.dumps([False, 'Не удалось отправить запрос на верификацию паспорта.']))

            subject, from_email, to = 'Запрос на верификацию паспорта', 'romanenko.anastasiya1998@yandex.ua', "romanenko.anastasiya1998@yandex.ua"
            text_content = 'Запрос на верификацию паспорта'

            # print(m)
            html_content = render_to_string('letter_verify_passport.html',
                                            {"surename": surename, "name": name, "passport": passport, "photo": photo})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponseRedirect("/profile/settings")
        else:
            return HttpResponseRedirect("/login")


def Buy_pro(request):
    layout, username, photo, balance, bonus = layout_name(request)
    user = request.session.get('username', 0)
    contact = layout_contact()
    link = layout_link()
    if user == 0:
        return HttpResponseRedirect("/login")
    else:
        user = Users.objects.get(auth_user__username=user)
        user_sub = UserSubcategories.objects.filter(user=user.auth_user)
        user_sub_list = []
        for i in user_sub:
            if i.subcategories.category.id not in user_sub_list:
                user_sub_list.append(i.subcategories.category.id)
        category = Category.objects.filter(id__in=user_sub_list).order_by('name')

        user_sub_list = []
        for i in user_sub:
            if i.subcategories.id not in user_sub_list:
                user_sub_list.append(i.subcategories.id)
        price_week = Services.objects.get(back_name='pro').price_week
        price_month = Services.objects.get(back_name='pro').price
        return render(request, 'Profile/Buy_pro.html', locals())


def profile_set_pro(request):
    string_id = request.GET.get('string_id')
    time = request.GET.get('time')
    end = ''
    if (time == 'week'):
        end = datetime.datetime.now()
        end += datetime.timedelta(days=7)
    else:
        days_in_month = calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[1]
        end += datetime.timedelta(days=days_in_month)
    user = request.session.get('username', 0)
    print(user)
    if user != 0:
        us = AuthUser.objects.get(username=user)
        id_list = string_id.split('|')
        for id in id_list:
            if id != "":
                id = id.split('_')[2]
                sub = SubCategory.objects.get(id=id)
                user_pro = UserPro(user=us, subcategory=sub, end_date=end)
                user_pro.save()
    return HttpResponse(json.dumps('good'))
