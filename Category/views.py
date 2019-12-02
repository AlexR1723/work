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

# Create your views here.
def All_category(request):
    layout, username = layout_name(request)
    contact=layout_contact()
    link=layout_link()
    city,regs,regions=layout_regions_cities(request)
    category = Category.objects.all()
    return render(request, 'Category/All_category.html', locals())

def Category_item(request,name):
    layout, username = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name=str(name).lower()
    category_item=Category.objects.get(name__icontains=name)
    subs=SubCategory.objects.filter(category_id=category_item.id)
    return render(request, 'Category/Category_item.html', locals())

def SubCategory(request,name):
    layout, username = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name=str(name).lower()
    sub=SubCategory().objects.get(name__icontains=name)
    # subs=SubCategory.objects.filter(category_id=category_item.id)
    return render(request, 'Category/Sub_category.html', locals())

