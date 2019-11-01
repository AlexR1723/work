from django.shortcuts import render

# Create your views here.
def All_category(request):
    return render(request, 'Category/All_category.html', locals())