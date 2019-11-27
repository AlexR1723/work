from django.shortcuts import render
from .models import *

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

# Create your views here.
def All_category(request):
    contact=layout_contact()
    link=layout_link()
    city,regs,regions=layout_regions_cities(request)
    category = Category.objects.all()
    return render(request, 'Category/All_category.html', locals())

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
    return render(request, 'Category/Category_item.html', locals())