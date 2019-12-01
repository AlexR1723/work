from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
import random
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.core.validators import validate_email
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse

def layout_contact():
    contact=ContactType.objects.all()
    return contact

def layout_link():
    link=Link.objects.all()
    return link

# def layout_regions():
#     regions = Region.objects.all()
#     return regions

def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg,regions

# Create your views here.
def Main(request):
    layout='layout_customer.html'
    # layout = 'layout.html'
    contact=layout_contact()
    link=layout_link()
    city,regs,regions=layout_regions_cities(request)

    fslide=FirstSlider.objects.all()[0]
    slide=FirstSlider.objects.all()[1:]
    category=Category.objects.all().order_by('id')[:3]
    all_category=Category.objects.all().order_by('id')[3:]


    # subs=SubCategory.objects.all()
    # for i in subs:
    #     name = i.name
    #     inc=0
    #     for j in subs:
    #         if j.name==name:
    #             inc=inc+1
    #     if inc>1:
    #         print(str(i.id) +' '+i.name)

    # str='Распространение рекламы#Услуги промоутеров#Изготовление и монтаж наружной рекламы#Услуги звукорежиссера#Реклама в Интернете#Услуги модели#Другая реклама'
    # list_str=str.split('#')
    # models.Feedback.objects.create(name=name, phonenumber=phone, text=text) 6
    # print(list_str)
    # for i in list_str:
    #     SubCategory.objects.create(category_id=14,name=i)

    return render(request, 'Main/Main.html', locals())

def How_it_work(request):
    contact = layout_contact()
    link = layout_link()
    seo=OrderService.objects.all()
    city, regs, regions = layout_regions_cities(request)

    # city = request.session.get('city', 0)
    # reg = request.session.get('reg', 0)
    # print(city)
    # print(reg)
    return render(request, 'Main/How_it_works.html', locals())


def Secure_transaction(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    what = WhatSafe.objects.all()
    benefits = BenefitsSafe.objects.all()
    return render(request, 'Main/Secure_transaction.html', locals())


def Safety(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)
    return render(request, 'Main/Safety.html', locals())


def Rabota(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    whyme = WhyWe.objects.all().order_by('id')
    seo = BecomePerformer.objects.all()

    category=Category.objects.all().order_by('name')
    # cat=category
    sub=SubCategory.objects.values('category_id')
    # sub=SubCategory.objects.all().order_by('name')
    # print(sub[0].category_id)
    # for i in sub:
    #     # print(i.category_id)
    #     i.category_id=cat.get(id=i.category_id)
    # print(sub[0].category_id)
    #
    list=[]
    for i in category:
        list1=[]
        list1.append(i.name)
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/Rabota.html', locals())


def For_business(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    category = Category.objects.all().order_by('name')
    sub = SubCategory.objects.values('category_id')

    list = []
    for i in category:
        list1 = []
        list1.append(i.name)
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/For_business.html', locals())


def Top_performers(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)
    return render(request, 'Main/Top_performers.html', locals())


def Dev(request):
    id = request.GET.get('id')
    print(id)
    # if id:

    return render(request, 'Main/Dev.html', locals())

def Dev(request,text):
    # id = request.GET.get('id')
    print(text)
    id=text
    # if id:

    return render(request, 'Main/Dev.html', locals())


def Test(request):
    return render(request, 'Test.html', locals())


def Login(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Login.html', locals())


def Register(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Register.html', locals())

def Question_details(request):
    return render(request, 'Main/Question_details.html', locals())

def login_user(request):
    email = request.GET.get("email")
    password = request.GET.get("pass")

    # if len(password)<8:
    #     return HttpResponse(json.dumps('Пароль не менее 8 символов'))
    if len(password)==0 or len(email)==0:
        # return HttpResponse(json.dumps('Заполните поля!'))
        return HttpResponse(json.dumps(False))

    try:
        check_email=validate_email(email)
    # if validate_email(email) == False or len(password) < 8:

    except:
        return HttpResponse(json.dumps('Поля заполнены неверно!'))


    user = authenticate(username=email, password=password)

    if user is None:
        return HttpResponse(json.dumps('Логин или пароль введены неверно!'))
    else:
        login(request, user)
        request.session['username'] = AuthUser.objects.get(id=user.id).username
        request.session.modified = True
        return HttpResponse(json.dumps(True))

@transaction.atomic
def Registrate(request):
    name = request.GET.get("name")
    surname = request.GET.get("surname")
    email = request.GET.get("email")
    tel = request.GET.get("tel")
    password = request.GET.get("pass1")
    list = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    try:
        key = ''
        us=AuthUser.objects.all().filter(email=email)
        print(us)
        if (len(us) == 0):
            key = ''
            while (len(key) < 50):
                i = random.randint(0, len(list) - 1)
                key += str(list[i])
            with transaction.atomic():
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.last_name=surname
                user.is_active=False
                user.save()
                auth_user = AuthUser.objects.filter(id=user.id)[0]
                print(auth_user)
                new_user=Users(auth_user=auth_user,phone=tel,uuid=key)
                new_user.save()
            subject, from_email, to = 'Верификация', 'romanenko.anastasiya1998@yandex.ua', email
            text_content = 'Перейдите по ссылке для автивации учетной записи.'
            m='https://work-proj.herokuapp.com/verify/'+key
            print(m)
            html_content=render_to_string('letter.html', {"key" : key})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse(json.dumps({'data': 'ok'}))
        else:
            return HttpResponse(json.dumps({'data': 'email'}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))

    # user=models.User(name=name,login=email,password=password)


def Verify(request, key):
    user = Users.objects.all().filter(uuid=key)
    print(user[0].auth_user)
    if(len(user)>0):
        us = AuthUser.objects.all().filter(id=user[0].auth_user.id)[0]
        us.is_active=True
        us.save()
    return render(request, 'Main/Login.html', locals())


def Public_offer(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    po = PublicOffer.objects.all().order_by('number')
    public_offer = []
    for i in po:
        po1 = []
        po1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        po2 = []
        for j in arr:
            po2.append(j)
        po1.append(po2)
        public_offer.append(po1)
    return render(request, 'Main/Public_offer.html', locals())

def Rules(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    rl = ProjectRules.objects.all().order_by('number')
    rules = []
    for i in rl:
        rl1 = []
        rl1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        rl2 = []
        for j in arr:
            rl2.append(j)
        rl1.append(rl2)
        rules.append(rl1)
    return render(request, 'Main/Rules.html', locals())

def Privacy_rules(request):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    pr=PrivacyRules.objects.all().order_by('number')
    privacy_rules=[]
    for i in pr:
        pr1=[]
        pr1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        pr2=[]
        for j in arr:
            pr2.append(j)
        pr1.append(pr2)
        privacy_rules.append(pr1)
    return render(request, 'Main/Privacy_rules.html', locals())

# def Search_results_help(request,name):
#     contact = layout_contact()
#     link = layout_link()
#     city,regs,regions=layout_regions_cities(request)
#
#     name = str(name).lower()
#     results = HelpCategory.objects.get(name__icontains=name)
#     # id=category_item.id
#
#     subs = HelpSubcategory.objects.filter(help_category=results.id)
#     count =subs.count()
#
#     return render(request, 'Main/Search_results.html', locals())



def Find_category(request, text):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    # print(text)
    id=text

    return render(request, 'Main/Dev.html', locals())

def search_input_category(request):
    cat = []
    res_cat = Category.objects.all()
    for i in res_cat:
        cat1 = []
        cat1.append(i.id)
        cat1.append(i.name)
        cat.append(cat1)

    subcat=[]
    res_subcat = SubCategory.objects.all()
    for i in res_subcat:
        subcat1=[]
        subcat1.append(i.name)
        subcat1.append(i.category_id)
        subcat.append(subcat1)
    list=[]
    list.append(cat)
    list.append(subcat)

    return HttpResponse(json.dumps(list))

def Search_results_help(request,name):
    in_name=name
    name=str(name).lower()
    subs=HelpSubcategory.objects.filter(text__icontains=name).values('id','text')
    count=subs.count()
    # return HttpResponse(json.dumps(subs))
    return render(request, 'Main/Search_results.html', locals())

def set_session_city(request):
    choosen_city = str(request.GET.get("city")).lower()
    choosen_reg = str(request.GET.get("reg")).lower()
    print(choosen_reg)
    print(choosen_city)
    try:
        exist_reg=Region.objects.get(name__icontains=choosen_reg)
        exist_city = City.objects.get(name__icontains=choosen_city,region=exist_reg.id)
    # if exist_reg and exist_city:
        request.session['reg'] = exist_reg.name
        request.session['city'] = exist_city.name
        request.session.modified = True
        return HttpResponse(json.dumps('good'))
    # else:
    except:
        return HttpResponse(json.dumps('bad'))
