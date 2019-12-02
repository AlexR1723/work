from django.shortcuts import render
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

import json
import random
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
# from django.contrib.auth.hashers import *
import re
from django.contrib.auth import authenticate, login, logout

from distutils.util import strtobool

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
def layout_name(request):
    layout = 'layout.html'
    username=''
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout,username

# Create your views here.
def Profile_settings(request):
    layout, username = layout_name(request)
    if(username != ''):
        email = request.session.get('username', 'no')
        user=Users.objects.all().filter(auth_user__email=email)[0]
        day=user.birthday.day
        if(day<10):
            day = '0' + str(user.birthday.day)
        month = user.birthday.month
        if(month<10):
            month='0'+str(user.birthday.month)
        year=user.birthday.year
        print(str(user.birthday.day)+'.'+str(user.birthday.month)+'.'+str(user.birthday.year))
        return render(request, 'Profile/Profile_settings.html', locals())
    else:
        return HttpResponseRedirect("/login")


# def Profile_edit(request):
#     layout, username = layout_name(request)
#     if (username != ''):
#         email = request.session.get('username', 'no')
#         user = Users.objects.all().filter(auth_user__email=email)[0]
#         return render(request, 'Profile/Profile_edit.html', locals())
#     else:
#         return HttpResponseRedirect("/login")


def Save(request):
    if request.method == 'POST':
        # doc = request.FILES
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        gender=''
        if(request.POST.get('gender')==1):
            gender=Gender.objects.all().filter(name="Мужской")[0]
        else:
            gender = Gender.objects.all().filter(name="Женский")[0]
        user.birthday=request.POST.get('birthday')
        user.gender_id=gender
        user.about_me=request.POST.get('about')
        user.save()

    return HttpResponseRedirect("/profile/settings")

def Save_phone(request):
    if request.method == 'POST':
        email = request.session.get('username', 'no')
        user = Users.objects.all().filter(auth_user__email=email)[0]
        user.phone=request.POST.get('phone')
        user.save()

    return HttpResponseRedirect("/profile/settings")


def Choose_city(request):
    layout, username = layout_name(request)

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


def Adverts_add(request):
    layout, username = layout_name(request)
    if (username != ''):
        return render(request, 'Profile/Adverts_add.html', locals())
    else:
        return HttpResponseRedirect("/login")


def Choose_categ(request):
    layout, username = layout_name(request)

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
                    # AuthUser.objects.filter(id=user_id).update(password=new_pass)
                    set_pass = AuthUser.objects.get(id=user_id)
                    set_pass.password = new_pass
                    set_pass.save()
                    # user =AuthUser.objects.get(id=user_id)
                    # user.set
                    # AuthUser.save(self)
                    # return HttpResponse(json.dumps('Пароли изменён!'))
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

    # time=request.session.get_expiry_age()
    # print(time/60/60/24)
    # date = request.session.get_expiry_date()
    # print(date)

    return HttpResponse(json.dumps(list))
    # response = HttpResponse({"error": "there was an error"})
    # response.status_code = 403  # To announce that the user isn't allowed to publish
    # return response

def load_photos(request):
    files=request.GET.get('files')
    files=request.FILES['newsslide']
    print(files)

    return HttpResponse(json.dumps('good'))

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
            # UserCities.objects.create(user_id=us,cities_id=city)
        else:
            UserCities.objects.get(user_id=us, city_id=city).delete()
            # UserCities.objects.get(user_id=us, cities_id=city).delete()
    return HttpResponse(json.dumps('good'))