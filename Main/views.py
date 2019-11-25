from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
# from django.forms.models import model_to_dict as to_js
import json
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

def Test(request):
    return render(request, 'Test.html', locals())

def Login(request):
    return render(request, 'Main/Login.html', locals())

def Register(request):
    return render(request, 'Main/Register.html', locals())

def Public_offer(request):
    return render(request, 'Main/Public_offer.html', locals())

def Rules(request):
    return render(request, 'Main/Rules.html', locals())

def Privacy_rules(request):
    return render(request, 'Main/Privacy_rules.html', locals())

def Search_results(request):
    return render(request, 'Main/Search_results.html', locals())

def Question_category(request):
    return render(request, 'Main/Question_category.html', locals())

def Category_item(request):
    return render(request, 'Main/Category_item.html', locals())

def Profile_settings(request):
    return render(request, 'Main/Profile_settings.html', locals())

def Help(request):
    contact = layout_contact()
    link = layout_link()
    # quest=HelpCategory.objects.a
    category=HelpCategory.objects.all()
    return render(request, 'Main/Help.html', locals())

def search_input(request):
    word = request.GET.get("word")
    word = str(word).strip()
    print(word)
    res=SubCategory.objects.filter(name__icontains=word)[:6]
    # list = models.Products.objects.all()
    # list1 = []
    # for i in list:
    #     list2 = []
    #     list2.append(i.id)
    #     list2.append(i.name.lower())
    #     list1.append(list2)
    # return HttpResponse(json.dumps({'data': res}))
    #     obj = MyModel.objects.get(pk=id)
    list=[]
    for i in res:
        list1=[]
        list1.append(i.id)
        list1.append(i.name)
        list1.append(Category.objects.get(id=i.category_id).name)
        list.append(list1)

    # data = serializers.serialize('json', res,fields=('name'))
    # struct = json.loads(data)
    # data = json.dumps(struct[0])
    # return HttpResponse(data, mimetype='application/json')
    # return HttpResponse(word)
    # obj=to_js(res)
    return HttpResponse(json.dumps(list))