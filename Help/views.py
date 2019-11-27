from django.shortcuts import render
from .models import *

# Create your views here.
def layout_contact():
    contact=ContactType.objects.all()
    return contact

def layout_link():
    link=Link.objects.all()
    return link

def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg,regions


def Help(request):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    # quest=HelpCategory.objects.a
    category = HelpCategory.objects.all()
    return render(request, 'Help/Help.html', locals())


def Question_category(request,name):
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Help/Question_category.html', locals())


def Search_results(request,name):
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name = str(name).lower()
    results = HelpCategory.objects.get(name__icontains=name)
    # id=category_item.id

    subs = HelpSubcategory.objects.filter(help_category=results.id)
    count =subs.count()

    return render(request, 'Help/Search_results.html', locals())