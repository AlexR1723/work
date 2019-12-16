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

list_page = []
advert_count = 0

# Create your views here.
def Advert(request):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    advert_count = UserAdvert.objects.all().order_by('-date').count()
    if( advert_count > 10):
        advert=UserAdvert.objects.all().order_by('-date')[0:10]
    else:
        advert = UserAdvert.objects.all().order_by('-date')[0:]
    k = 0
    while (advert_count > 0):
        k = k + 1
        advert_count = advert_count - 10
    list_page = []
    page = 1
    if (k > 6):
        for i in range(1, 4):
            list_page.append(i)
        list_page.append('...')
        for i in range(k - 2, k + 1):
            list_page.append(i)
    else:
        for i in range(1, k + 1):
            list_page.append(i)
    pre = 1
    next = page + 1
    return render(request, 'Advert/Advert.html', locals())

def Advert_page(request,page):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    page = int(page)
    start = page * 10 - 10
    end = page * 10
    advert_count = UserAdvert.objects.all().order_by('-date').count()
    advert=UserAdvert.objects.all().order_by('-date')[start:end]

    k = 0
    while (advert_count > 0):
        k = k + 1
        advert_count = advert_count - 10
    Page = []
    if k > 6:
        # записать первые 3
        for i in range(1, 4):
            Page.append(i)
        # записать середину
        if page >= 3 and page <= (k - 2):
            for i in range(page - 1, page + 2):
                Page.append(i)
        # записать последние 3
        for i in range(k - 2, k + 1):
            Page.append(i)
    else:
        for i in range(1, k + 1):
            Page.append(i)
    # убрать повторения
    Page = list(set(Page))
    print(Page)
    list_page = []
    # добавить '...'
    for i in range(len(Page) - 1):
        list_page.append(Page[i])
        if Page[i + 1] - Page[i] > 1:
            list_page.append('...')
    list_page.append(Page[len(Page) - 1])
    pre = page - 1
    next = page + 1
    return render(request, 'Advert/Advert.html', locals())

def Adverts_detail(request,id):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    id=int(id)
    advert = (UserAdvert.objects.all().filter(id=id))[0]
    advert_photo=UserAdvertPhoto.objects.all().filter(advert_id=id)
    sub = SubCategory.objects.filter(name__icontains = advert.subcategory.name)
    print(sub)
    return render(request, 'Advert/Advert_detail.html', locals())
