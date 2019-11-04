from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link

list_page = []
news_count = 0


def New(request):
    contact=layout_contact()
    link=layout_link()
    filter = 0

    news_type=NewsType.objects.all()
    news=News.objects.all().order_by('-date')[0:10]

    news_count = News.objects.order_by('-date').count()
    k = 0
    while (news_count > 0):
        k = k + 1
        news_count = news_count - 10
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
    return render(request, 'News/News.html', locals())

def News_page(request,page):
    contact = layout_contact()
    link = layout_link()
    filter=0

    news_type = NewsType.objects.all()

    page=int(page)
    start=page*10-10
    end=page*10
    news=News.objects.all().order_by('-date')[start:end]

    news_count = News.objects.order_by('-date').count()
    k =0
    while (news_count > 0):
        k = k + 1
        news_count = news_count - 10
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
    return render(request, 'News/News.html', locals())

def News_detail(request, id):
    return render(request, 'News/News_detail.html', locals())

def News_filter(request, filter):
    print('filter')
    contact = layout_contact()
    link = layout_link()
    filter=str(filter)

    news_type = NewsType.objects.all()
    news = News.objects.all().order_by('-date').filter(type__name=filter)[0:10]


    news_count = News.objects.order_by('-date').filter(type__name=filter).count()
    print(news_count)
    k = 0
    while (news_count > 0):
        k = k + 1
        news_count = news_count - 10
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
    print(list_page)
    return render(request, 'News/News.html', locals())

def News_filter_page(request, filter,page):
    contact = layout_contact()
    link = layout_link()
    filter = str(filter)

    news_type = NewsType.objects.all()

    page = int(page)
    start = page * 10 - 10
    end = page * 10
    news = News.objects.all().order_by('-date').filter(type__name=filter)[start:end]

    news_count = News.objects.order_by('-date').filter(type__name=filter).count()
    k = 0
    while (news_count > 0):
        k = k + 1
        news_count = news_count - 10
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
    return render(request, 'News/News.html', locals())