from django.shortcuts import render
from .models import *

def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link

# Create your views here.
def Contact(request):
    contact = layout_contact()
    link = layout_link()
    return render(request, 'Contact/Contact.html', locals())