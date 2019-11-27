from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core import serializers
import json
import random
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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
# def layout_cities():
#     cities = City.objects.all()
#     return cities


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
    city,regs,regions=layout_regions_cities(request)
    # city_dnr = City.objects.filter(region_id=(Region.objects.filter(name='ДНР')[0].id)).order_by('name')
    # city_lnr = City.objects.filter(region_id=(Region.objects.filter(name='ЛНР')[0].id)).order_by('name')
    # city_rus = City.objects.filter(region_id=(Region.objects.filter(name='Россия')[0].id)).order_by('name')
    # city_ukr = City.objects.filter(region_id=(Region.objects.filter(name='Украина')[0].id)).order_by('name')

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

def Test(request):
    return render(request, 'Test.html', locals())

def Login(request):
    return render(request, 'Main/Login.html', locals())

def Register(request):
    # list = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    # key=''
    # while (len(key)<50):
    #     i=random.randint(0,len(list)-1)
    #     key+=str(list[i])
    # print(key)
    return render(request, 'Main/Register.html', locals())

def Registrate(request):
    name = request.GET.get("name")
    surname = request.GET.get("surname")
    email = request.GET.get("email")
    tel = request.GET.get("tel")
    password = request.GET.get("pass1")
    list = [1,2,3,4,5,6,7,8,9,0,'a','b','c','d','e','f','g','h','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    try:
        key = ''
        while (len(key) < 50):
            i = random.randint(0, len(list) - 1)
            key += str(list[i])
        user = User.objects.create_user(email, email, password)
        user.first_name = name
        user.last_name=surname
        user.save()
        print('1')
        new_user=Users(auth_user=user.id, phone=tel,uuid=key)
        print('2')
        new_user.save()
        print('3')
    except:
        print('error')
    return HttpResponse(json.dumps({'data': 'ok'}))

    # user=models.User(name=name,login=email,password=password)



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

def Search_results(request,name):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name = str(name).lower()
    results = HelpCategory.objects.get(name__icontains=name)
    # id=category_item.id

    subs = HelpSubcategory.objects.filter(help_category=results.id)
    count =subs.count()

    return render(request, 'Main/Search_results.html', locals())

def Question_category(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Question_category.html', locals())


def Category_item(request,name):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name=str(name).lower()
    category_item=Category.objects.get(name__icontains=name)
    # id=category_item.id
    subs=SubCategory.objects.filter(category_id=category_item.id)


    # all_cat=Category.objects.all()
    # for i in all_cat:
    #     i.text="Описание категории "+i.name+" vehicula ipsum a arcu cursus vitae congue mauris rhoncus aenean vel elit scelerisque mauris pellentesque pulvinar pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas maecenas"
    #     i.save()
    return render(request, 'Main/Category_item.html', locals())

def Help(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    # quest=HelpCategory.objects.a
    category = HelpCategory.objects.all()
    return render(request, 'Main/Help.html', locals())

def search_input(request):
    # word = request.GET.get("word")
    # word = str(word).strip()
    # print(word)
    # arr=word.split(' ')
    # res=SubCategory.objects.filter(name__icontains=word)[:6]
    # if arr.count()>1:
    #     list = res=SubCategory.objects.filter(name__icontains=arr[0])
    #     for i in range(arr.count() - 1):
    #         if(list[])
    #
    # else:
    #     res=SubCategory.objects.filter(name__icontains=arr[0])[:10]


    # list = models.Products.objects.all()
    # list1 = []
    # for i in list:
    #     list2 = []
    #     list2.append(i.id)
    #     list2.append(i.name.lower())
    #     list1.append(list2)
    # return HttpResponse(json.dumps({'data': res}))
    #     obj = MyModel.objects.get(pk=id)
    cat = []
    res_cat = Category.objects.all()
    for i in res_cat:
        cat1 = []
        cat1.append(i.id)
        cat1.append(i.name)
        # list1.append(Category.objects.get(id=i.category_id).name)
        # subcat1.append(i.category_id)
        cat.append(cat1)

    subcat=[]
    res_subcat = SubCategory.objects.all()
    for i in res_subcat:
        subcat1=[]
        subcat1.append(i.id)
        subcat1.append(i.name)
        # list1.append(Category.objects.get(id=i.category_id).name)
        # subcat1.append(res_cat.get(id=i.category_id).name)
        subcat1.append(i.category_id)
        subcat.append(subcat1)

    # data = serializers.serialize('json', res,fields=('name'))
    # struct = json.loads(data)
    # data = json.dumps(struct[0])
    # return HttpResponse(data, mimetype='application/json')
    # return HttpResponse(word)
    # obj=to_js(res)
    count1=SubCategory.objects.count()
    count1=SubCategory.objects.count()
    count1=SubCategory.objects.count()
    count1=SubCategory.objects.count()

    list=[]
    list.append(cat)
    list.append(subcat)

    return HttpResponse(json.dumps(list))

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
