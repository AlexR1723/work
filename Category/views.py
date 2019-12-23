from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

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

# Create your views here.
def All_category(request):
    layout, username, photo = layout_name(request)
    contact=layout_contact()
    link=layout_link()
    city,regs,regions=layout_regions_cities(request)
    category = Category.objects.all()
    return render(request, 'Category/All_category.html', locals())

def Category_item(request,name):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    name=str(name).lower()
    category_item=Category.objects.get(name__icontains=name)
    subs=SubCategory.objects.filter(category_id=category_item.id)

    task_count=UserTask.objects.all().filter(subcategory__category=category_item).filter(task_status__name="В поиске").order_by('-date').count()
    print(task_count)
    if(task_count<10):
        task=UserTask.objects.all().filter(subcategory__category=category_item).filter(task_status__name="В поиске").order_by('-date')[0:]
    else:
        task = UserTask.objects.all().filter(subcategory__category=category_item).filter(task_status__name="В поиске").order_by('-date')[0:10]
    return render(request, 'Category/Category_item.html', locals())

list_page = []
sub_count = 0

def sub_category(request,name):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)

    # name=str(name).lower()
    # print('start')
    sub = SubCategory.objects.filter(name__icontains=name)
    # if sub.count() > 1:
    #     if username=='':
    #         return HttpResponseRedirect("/login")
    #     else:
    #         return HttpResponseRedirect("/profile/create_task/"+name)
    # else:

    advert_count = UserAdvert.objects.all().filter(subcategory=sub[0]).order_by('-date').count()
    count_user=UserSubcategories.objects.all().filter(subcategories=sub[0]).count()
    if(advert_count<10):
        advert=UserAdvert.objects.all().filter(subcategory=sub[0]).order_by('-date')[0:]
    else:
        advert=UserAdvert.objects.all().filter(subcategory=sub[0]).order_by('-date')[0:10]

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
    return render(request, 'Category/Sub_category.html', locals())

def Page_subcategory(request,name,page):
    layout, username, photo = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city,regs,regions=layout_regions_cities(request)
    filter=0


    page=int(page)
    start=page*10-10
    end=page*10
    sub=SubCategory.objects.get(name__icontains=name)
    advert = UserAdvert.objects.all().filter(subcategory=sub).order_by('-date')[start:end]
    count_user = UserSubcategories.objects.all().filter(subcategories=sub).count()

    advert_count = UserAdvert.objects.all().filter(subcategory=sub).order_by('-date').count()

    k =0
    while (advert_count > 0):
        k = k + 1
        advert_count = advert_count - 10
    Page = []
    if k>6:
        # записать первые 3
        for i in range(1,4):
            Page.append(i)
        # записать середину
        if page >= 3 and page <= (k - 2):
            for i in range(page - 1, page + 2):
                Page.append(i)
        # записать последние 3
        for i in range(k - 2, k+1):
            Page.append(i)
    else:
        for i in range(1,k+1):
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
    pre = page-1
    next = page+1
    return render(request, 'Category/Sub_category.html', locals())