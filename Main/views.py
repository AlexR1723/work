from django.shortcuts import render
import models

# Create your views here.
def Main(request):
    return render(request, 'Main/Main.html', locals())

def About(request):
    return render(request, 'Main/About.html', locals())