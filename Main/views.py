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
    category=Category.objects.all()[:3]
    all_category=Category.objects.all()[3:]
    return render(request, 'Main/Main.html', locals())

def How_it_work(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/How_it_works.html', locals())

def Secure_transaction(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Secure_transaction.html', locals())

def Safety(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Safety.html', locals())

def Rabota(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Rabota.html', locals())

def For_business(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/For_business.html', locals())

def Top_performers(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Main/Top_performers.html', locals())


