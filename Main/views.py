from django.shortcuts import render
import models

# Create your views here.
def Main(request):
    return render(request, 'Main/Main.html', locals())

def About(request):
    return render(request, 'Main/About.html', locals())

def Contact(request):
    return render(request, 'Main/Contact.html', locals())

def News(request):
    return render(request, 'Main/News.html', locals())

def news_detail(request):
    return render(request, 'Main/News_detail.html', locals())

def how_it_work(request):
    return render(request, 'Main/How_it_works.html', locals())

def secure_transaction(request):
    return render(request, 'Main/Secure_transaction.html', locals())

def safety(request):
    return render(request, 'Main/Safety.html', locals())

def Top_performers(request):
    return render(request, 'Main/Top_performers.html', locals())

def All_category(request):
    return render(request, 'Main/All_category.html', locals())