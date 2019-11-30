from django.shortcuts import render

# Create your views here.
def Profile_settings(request):
    return render(request, 'Profile/Profile_settings.html', locals())

def Choose_city(request):
    return render(request, 'Profile/Choose_city.html', locals())

def Adverts_add(request):
    return render(request, 'Profile/Adverts_add.html', locals())

def Choose_categ(request):
    return render(request, 'Profile/Choose_categ.html', locals())
