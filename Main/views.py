from django.shortcuts import render
import models

# Create your views here.
def Main(request):
    return render(request, 'Main/Main.html', locals())

def How_it_work(request):
    return render(request, 'Main/How_it_works.html', locals())

def Secure_transaction(request):
    return render(request, 'Main/Secure_transaction.html', locals())

def Safety(request):
    return render(request, 'Main/Safety.html', locals())

def Top_performers(request):
    return render(request, 'Main/Top_performers.html', locals())


