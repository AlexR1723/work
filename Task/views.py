from django.shortcuts import render
from .models import *
# Create your views here.
def layout_contact():
    contact=ContactType.objects.all()
    return contact
def layout_link():
    link=Link.objects.all()
    return link
def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg,regions

def layout_name(request):
    layout = 'layout.html'
    username=''
    photo=''
    balance = 0
    bonus = 0
    user = request.session.get('username', 'no')
    if (user != 'no'):
        username=AuthUser.objects.all().filter(email=user)[0].first_name
        photo=Users.objects.all().filter(auth_user__email=user)[0].photo
        user = Users.objects.all().filter(auth_user__email=user)[0]
        balance = user.balance
        bonus = user.bonus_balance
        if (user.type.name == "Заказчик"):
            layout = 'layout_customer.html'
        else:
            layout = 'layout_executor.html'
    return layout, username, photo, balance, bonus


def is_verify(request):
    if (request.session.get('username', 'no') != 'no'):
        verify = True
    else:
        verify = False
    return verify


list_page = []
advert_count = 0

def Task(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    category = Category.objects.all().order_by('name')

    return render(request, 'Task/Task.html', locals())

def Tasks_detail(request, id):
    layout, username, photo, balance, bonus = layout_name(request)
    id=int(id)
    task=UserTask.objects.get(id=id)
    sub=task.subcategory
    verify = is_verify(request)
    task_bet=UserTaskBet.objects.filter(task=task).order_by('-date')
    name = request.session.get('username', 'no')
    user = AuthUser.objects.filter(email=name)[0]
    is_pro=UserPro.objects.filter(subcategory=sub).filter(user=user).count()
    is_bet=UserTaskBet.objects.filter(task=task).filter(user=user).count()
    print(is_pro)
    return render(request, 'Task/Task_detail.html', locals())