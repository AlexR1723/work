from django.shortcuts import render

# Create your views here.
def Advert(request):
    return render(request, 'Task/Task.html', locals())