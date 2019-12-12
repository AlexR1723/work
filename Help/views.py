from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json


# Create your views here.
def layout_contact():
    contact = ContactType.objects.all()
    return contact


def layout_link():
    link = Link.objects.all()
    return link

def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg, regions

def layout_name(request):
    layout = 'layout.html'
    username=''
    photo=''
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        photo=Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout,username,photo

def Help(request):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    category = HelpCategory.objects.all()
    return render(request, 'Help/Help.html', locals())


def Question_category(request, name):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    name = str(name).lower()
    results = HelpCategory.objects.get(name__icontains=name)
    subs = HelpSubcategory.objects.filter(help_category=results.id)

    return render(request, 'Help/Question_category.html', locals())

def Find_help(request, text):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    subs=HelpSubcategory.objects.filter(text__icontains=text)
    count=subs.count()
    name=text

    return render(request, 'Help/Search_results.html', locals())

def questions(request, text):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    quest=HelpSubcategory.objects.get(text__icontains=text)
    desc=quest.description.split('\r\n')
    desc.remove('')
    name=quest.text

    images=HelpImages.objects.filter(question=quest.id)

    return render(request, 'Help/Question_details.html', locals())


def load_input_help(request):
    subhelp=[]
    res_subcat = HelpSubcategory.objects.all()
    for i in res_subcat:
        subhelp.append(i.text)
    return HttpResponse(json.dumps(subhelp))
