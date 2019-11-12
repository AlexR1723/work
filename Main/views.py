from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link

# Create your views here.
def Main(request):
    contact=layout_contact()
    link=layout_link()

    fslide=FirstSlider.objects.all()[0]
    slide=FirstSlider.objects.all()[1:]
    category=Category.objects.all().order_by('id')[:3]
    all_category=Category.objects.all().order_by('id')[3:]
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