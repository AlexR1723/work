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

def Top_performers(request):
    return render(request, 'Main/Top_performers.html', locals())