from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
def layout_regions():
    regions = Region.objects.all()
    return regions

# Create your views here.
def All_category(request):
    contact=layout_contact()
    link=layout_link()
    regions=layout_regions()
    category = Category.objects.all()
    return render(request, 'Category/All_category.html', locals())