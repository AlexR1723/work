from django.shortcuts import render

# Create your views here.
def News(request):
    return render(request, 'News/News.html', locals())

def News_detail(request):
    return render(request, 'News/News_detail.html', locals())