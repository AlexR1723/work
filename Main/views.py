from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
# def region_city():
    # city=City.objects.all()
    # region=Region.objects.all()
    # city_dnr=City.objects.filter(region_id=(Region.filter(name='ДНР')[0].id)).order_by('name')
    # city_lnr=City.objects.filter(region_id=(Region.filter(name='ЛНР')[0].id)).order_by('name')
    # city_rus=City.objects.filter(region_id=(Region.filter(name='Россия')[0].id)).order_by('name')
    # city_urk=City.objects.filter(region_id=(Region.filter(name='Украина')[0].id)).order_by('name')
    # print(city_dnr)
    # city1=[]
    # city1.append(city_dnr)
    # city1.append(city_dnr1)
    # return city_dnr

# Create your views here.
def Main(request):
    contact=layout_contact()
    link=layout_link()
    city_dnr = City.objects.filter(region_id=(Region.objects.filter(name='ДНР')[0].id)).order_by('name')
    city_lnr = City.objects.filter(region_id=(Region.objects.filter(name='ЛНР')[0].id)).order_by('name')
    city_rus = City.objects.filter(region_id=(Region.objects.filter(name='Россия')[0].id)).order_by('name')
    city_ukr = City.objects.filter(region_id=(Region.objects.filter(name='Украина')[0].id)).order_by('name')

    fslide=FirstSlider.objects.all()[0]
    slide=FirstSlider.objects.all()[1:]
    category=Category.objects.all().order_by('id')[:3]
    all_category=Category.objects.all().order_by('id')[3:]


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
    return render(request, 'Main/How_it_works.html', locals())

def Secure_transaction(request):
    contact = layout_contact()
    link = layout_link()

    what=WhatSafe.objects.all()
    benefits=BenefitsSafe.objects.all()
    return render(request, 'Main/Secure_transaction.html', locals())

def Safety(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Safety.html', locals())

def Rabota(request):
    contact = layout_contact()
    link = layout_link()

    whyme=WhyWe.objects.all().order_by('id')
    seo=BecomePerformer.objects.all()

    category=Category.objects.all().order_by('name')
    sub=SubCategory.objects.values('category_id')

    list=[]
    for i in category:
        list1=[]
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/Rabota.html', locals())

def For_business(request):
    contact = layout_contact()
    link = layout_link()

    category=Category.objects.all().order_by('name')
    sub=SubCategory.objects.values('category_id')

    list=[]
    for i in category:
        list1=[]
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/For_business.html', locals())

def Top_performers(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Top_performers.html', locals())

def Dev(request):
    return render(request, 'Main/Dev.html', locals())

def Login(request):
    return render(request, 'Main/Login.html', locals())
