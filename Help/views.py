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
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        user = Users.objects.all().filter(auth_user__email=user)[0]
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout,username


def Help(request):
    layout, username = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    # quest=HelpCategory.objects.a
    category = HelpCategory.objects.all()
    return render(request, 'Help/Help.html', locals())


def Question_category(request, name):
    layout, username = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    print('quest')

    name = str(name).lower()
    results = HelpCategory.objects.get(name__icontains=name)
    subs = HelpSubcategory.objects.filter(help_category=results.id)

    return render(request, 'Help/Question_category.html', locals())




# def Search_results(request, name):
#     contact = layout_contact()
#     link = layout_link()
#     city, regs, regions = layout_regions_cities(request)
#
#     name = str(name).lower()
#     results = HelpCategory.objects.get(name__icontains=name)
#     # id=category_item.id
#
#     subs = HelpSubcategory.objects.filter(help_category=results.id)
#     count = subs.count()
#
#     return render(request, 'Help/Search_results.html', locals())


def Find_help(request, text):
    layout, username = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    print(text)

    return render(request, 'Main/Dev.html', locals())

def load_input_help(request):
    # return HttpResponse(json.dumps(subhelp))
    # help = []
    # res_help = HelpCategory.objects.all()
    # for i in res_help:
    #     help1 = []
    #     help1.append(i.id)
    #     help1.append(i.name)
    #     help.append(help1)
    print('start')
    subhelp=[]
    res_subcat = HelpSubcategory.objects.all()
    print(res_subcat)
    for i in res_subcat:
    #     subhelp1=[]
        subhelp.append(i.text)
    #     subhelp1.append(i.text)
    #     subhelp1.append(i.help_category_id)
    #     subhelp.append(subhelp1)

    # list=[]
    # list.append(help)
    # list.append(subhelp)

    return HttpResponse(json.dumps(subhelp))

# def Search_results_help(request,name):
#     in_name=name
#     name=str(name).lower()
#     subs=HelpSubcategory.objects.filter(text__icontains=name).values('id','text')
#     count=subs.count()
#     # return HttpResponse(json.dumps(subs))
#     return render(request, 'Main/Search_results.html', locals())
