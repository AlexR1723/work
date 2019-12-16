from django.shortcuts import render

# Create your views here.
def Task(request):
    return render(request, 'Task/Task.html', locals())