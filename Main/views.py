from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, random,datetime
from .models import *
from django.contrib.auth import authenticate, login, logout, hashers
from django.contrib.auth.models import User
from django.db import transaction
from django.core.validators import validate_email
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse


def layout_contact():
    contact = ContactType.objects.all()
    return contact


def layout_link():
    link = Link.objects.all()
    return link


def layout_regions_cities(request):
    city = request.session.get('city', 0)
    reg = request.session.get('reg', 0)
    regions = Region.objects.all()
    return city, reg, regions


def layout_name(request):
    layout = 'layout.html'
    username = ''
    photo = ''
    balance = 0
    bonus = 0
    user = request.session.get('username', 'no')
    if (user != 'no'):
        if(AuthUser.objects.all().filter(email=user).count() >= 1):
            username = AuthUser.objects.all().filter(email=user)[0].first_name
            photo = Users.objects.all().filter(auth_user__email=user)[0].photo
            user = Users.objects.all().filter(auth_user__email=user)[0]
            balance = user.balance
            bonus = user.bonus_balance
            if (user.type.name == "Заказчик"):
                layout = 'layout_customer.html'
            else:
                layout = 'layout_executor.html'
        else:
            logout(request)
    return layout, username, photo, balance, bonus



def is_verify(request):
    if (request.session.get('username', 'no') != 'no'):
        verify = True
    else:
        verify = False
    return verify


# Create your views here.
def Main(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    verify = is_verify(request)

    fslide = FirstSlider.objects.all()[0]
    slide = FirstSlider.objects.all()[1:]
    category = Category.objects.all().order_by('id')[:3]
    all_category = Category.objects.all().order_by('id')[3:]

    count_executor = Users.objects.all().filter(type__name="Исполнитель").count()
    count_customer = Users.objects.all().filter(type__name="Заказчик").count()
    count_task = UserTask.objects.all()

    return render(request, 'Main/Main.html', locals())


def How_it_work(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    seo = OrderService.objects.all()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/How_it_works.html', locals())


def Secure_transaction(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    what = WhatSafe.objects.all()
    benefits = BenefitsSafe.objects.all()
    return render(request, 'Main/Secure_transaction.html', locals())


def Safety(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Safety.html', locals())


def Rabota(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    whyme = WhyWe.objects.all().order_by('id')
    seo = BecomePerformer.objects.all()

    category = Category.objects.all().order_by('name')
    sub = SubCategory.objects.values('category_id')
    list = []
    for i in category:
        list1 = []
        list1.append(i.name)
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/Rabota.html', locals())


def For_business(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    category = Category.objects.all().order_by('name')
    sub = SubCategory.objects.values('category_id')

    list = []
    for i in category:
        list1 = []
        list1.append(i.name)
        list1.append(i.image)
        list1.append(i.name)
        list1.append(sub.filter(category_id=i.id).count())
        list1.reverse()
        list.append(list1)

    return render(request, 'Main/For_business.html', locals())


def Top_performers(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Top_performers.html', locals())


def Dev(request):
    layout, username, photo, balance, bonus = layout_name(request)
    id = request.GET.get('id')
    print(id)

    return render(request, 'Main/Dev.html', locals())


def Login(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Login.html', locals())


def Register(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)
    return render(request, 'Main/Register.html', locals())




# def Question_details(request):
#     layout, username = layout_name(request)
#     return render(request, 'Main/Question_details.html', locals())
#
# def Sub_category(request):
#     layout, username = layout_name(request)
#     return render(request, 'Main/../templates/Category/Sub_category.html', locals())

def Task_details_performer(request):
    layout, username, photo, balance, bonus = layout_name(request)
    return render(request, 'Main/Task_details_performer.html', locals())

#
# def Task_details(request):
#     layout, username, photo = layout_name(request)
#     return render(request, 'Main/Task_details.html', locals())


def login_user(request):
    email = request.GET.get("email")
    password = request.GET.get("pass")
    if len(password) == 0 or len(email) == 0:
        return HttpResponse(json.dumps(False))

    try:
        check_email = validate_email(email)
    except:
        return HttpResponse(json.dumps('Поля заполнены неверно!'))

    user = authenticate(username=email, password=password)

    if user is None:
        return HttpResponse(json.dumps('Логин или пароль введены неверно!'))
    else:
        login(request, user)
        request.session['username'] = AuthUser.objects.get(id=user.id).username
        request.session.modified = True
        return HttpResponse(json.dumps(True))


@transaction.atomic
def Registrate(request):
    name = request.GET.get("name")
    surname = request.GET.get("surname")
    email = request.GET.get("email")
    tel = request.GET.get("tel")
    password = request.GET.get("pass1")
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    try:
        key = ''
        us = AuthUser.objects.all().filter(email=email)
        print(us)
        if (len(us) == 0):
            key = ''
            while (len(key) < 50):
                i = random.randint(0, len(list) - 1)
                key += str(list[i])
            with transaction.atomic():
                user = User.objects.create_user(email, email, password)
                user.first_name = name
                user.last_name = surname
                user.is_active=True
                # user.is_active = False
                user.save()
                auth_user = AuthUser.objects.filter(id=user.id)[0]
                print(auth_user)
                new_user = Users(auth_user=auth_user, photo="uploads/users/user.png", phone=tel, uuid=key,
                                 type=UserType.objects.all().filter(name="Исполнитель")[0])
                new_user.save()
            subject, from_email, to = 'Успешная регистрация', 'romanenko.anastasiya1998@yandex.ua', email
            text_content = 'Перейдите по ссылке для автивации учетной записи.'
            m = 'https://work-proj.herokuapp.com/verify/' + key
            print(m)
            html_content = render_to_string('letter.html', {"key": key, "email":email,"pass":password})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


            user_auth = authenticate(username=email, password=password)
            login(request, user_auth)
            request.session['username'] = AuthUser.objects.get(id=user_auth.id).username
            request.session.modified = True
            return HttpResponse(json.dumps(True))
        else:
            return HttpResponse(json.dumps({'data': 'email'}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))

    # user=models.User(name=name,login=email,password=password)


def Forgot(request):
    layout, username, photo, balance, bonus = layout_name(request)
    return render(request, 'Main/Forgot.html', locals())



def Page(request):
    layout, username, photo, balance, bonus = layout_name(request)
    return render(request, 'Main/Page.html', locals())

def send_new_pass(request):
    email = request.GET.get("email")
    print(email)
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    try:
        key = ''
        us = AuthUser.objects.all().filter(email=email)
        print(len(us))
        if (len(us) > 0):
            key=''
            print(key)
            while (len(key) < 8):
                i = random.randint(0, len(list) - 1)
                key += str(list[i])
            print(key)
            u = User.objects.get(username__exact=email)
            print(u)
            u.set_password(key)
            u.save()
            print(u)
            subject, from_email, to = 'Новый пароль', 'romanenko.anastasiya1998@yandex.ua', email
            text_content = 'Перейдите по ссылке для автивации учетной записи.'
            m = 'https://work-proj.herokuapp.com/verify/' + key
            print(m)
            html_content = render_to_string('forgot.html', {"email": email, "pass": key})
            print(html_content)
            # html_content="<a href='%s'>Активировать</a>" % m
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return HttpResponse(json.dumps(True))
        else:
            return HttpResponse(json.dumps({'data': 'email'}))
    except:
        return HttpResponse(json.dumps({'data': 'error'}))


def Verify(request, key):
    layout, username, photo, balance, bonus = layout_name(request)
    user = Users.objects.all().filter(uuid=key)
    print(user[0].auth_user)
    if (len(user) > 0):
        us = AuthUser.objects.all().filter(id=user[0].auth_user.id)[0]
        us.is_active = True
        us.save()
    return render(request, 'Main/Login.html', locals())


def Public_offer(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    po = PublicOffer.objects.all().order_by('number')
    public_offer = []
    for i in po:
        po1 = []
        po1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        po2 = []
        for j in arr:
            po2.append(j)
        po1.append(po2)
        public_offer.append(po1)
    return render(request, 'Main/Public_offer.html', locals())


def Rules(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    rl = ProjectRules.objects.all().order_by('number')
    rules = []
    for i in rl:
        rl1 = []
        rl1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        rl2 = []
        for j in arr:
            rl2.append(j)
        rl1.append(rl2)
        rules.append(rl1)
    return render(request, 'Main/Rules.html', locals())


def Privacy_rules(request):
    layout, username, photo, balance, bonus = layout_name(request)
    contact = layout_contact()
    link = layout_link()
    city, regs, regions = layout_regions_cities(request)

    pr = PrivacyRules.objects.all().order_by('number')
    privacy_rules = []
    for i in pr:
        pr1 = []
        pr1.append(i.header)
        arr = i.text.split("\n\r\n\r")
        pr2 = []
        for j in arr:
            pr2.append(j)
        pr1.append(pr2)
        privacy_rules.append(pr1)
    return render(request, 'Main/Privacy_rules.html', locals())


# def Find_category(request, text):
#     layout, username, photo = layout_name(request)
#     contact = layout_contact()
#     link = layout_link()
#     city, regs, regions = layout_regions_cities(request)
#
#     if username!='':
#         sub = SubCategory.objects.get(name__icontains=text)
#         # return render(request, 'Main/Dev.html', locals())
#         # return render(request, 'Main/Dev.html', locals())
#         return render(request, 'Category/Sub_category.html', locals())
#     # print(text)
#     # id=text
#
#     return render(request, 'Main/Dev.html', locals())

def search_input_category(request):
    cat = []
    res_cat = Category.objects.all()
    for i in res_cat:
        cat1 = []
        cat1.append(i.id)
        cat1.append(i.name)
        cat.append(cat1)

    subcat = []
    res_subcat = SubCategory.objects.all()
    for i in res_subcat:
        subcat1 = []
        subcat1.append(i.name)
        subcat1.append(i.category_id)
        subcat.append(subcat1)
    list = []
    list.append(cat)
    list.append(subcat)

    return HttpResponse(json.dumps(list))


def set_session_city(request):
    choosen_city = str(request.GET.get("city")).lower()
    choosen_reg = str(request.GET.get("reg")).lower()
    # print(choosen_reg)
    # print(choosen_city)
    try:
        exist_reg = Region.objects.get(name__icontains=choosen_reg)
        exist_city = City.objects.get(name__icontains=choosen_city, region=exist_reg.id)
        request.session['reg'] = exist_reg.name
        request.session['city'] = exist_city.name
        request.session.modified = True
        return HttpResponse(json.dumps('good'))
    except:
        return HttpResponse(json.dumps('bad'))


def get_counter_values(request):
    values = request.GET.get('values')
    values = str(values).split(',')
    # print('start')
    counters = {
        'register_exec': AuthUser.objects.count(),
        'register_perf': AuthUser.objects.count(),
        'count_tasks': UserTask.objects.count(),
        'today_create_tasks': UserTask.objects.filter(date=datetime.datetime.now().date()).count(),
        'complete_tasks': UserTask.objects.filter(task_status=UserTaskStatus.objects.get(name='Выполнено').id).count(),
        'count_users': Users.objects.count(),
        'avialable_tasks': UserTask.objects.filter(task_status=UserTaskStatus.objects.get(name='В поиске').id).count(),

    }
    results = []
    for i in values:
        try:
            res = int(counters[i])
        except:
            res = 0
        results.append(res)
    # print(datetime.date)
    # print(datetime.datetime.now().date())
    # print(UserTask.objects.filter(task_status=UserTaskStatus.objects.get(name='Выполнено'))[0].date)
    return HttpResponse(json.dumps(results))



# def Profile_verified(request):
#     layout, username, photo = layout_name(request)
#     return render(request, 'Main/Profile_verified.html', locals())

# def Awards(request):
#     layout, username, photo = layout_name(request)
#     return render(request, 'Main/../templates/Profile/Awards.html', locals())
#
# def Number_verification(request):
#     layout, username, photo = layout_name(request)
#     return render(request, 'Main/../templates/Profile/Number_verification.html', locals())

# def Passport_verification(request):
#      layout, username, photo = layout_name(request)
#      return render(request, 'Main/../templates/Profile/Passport_verification.html', locals())

def Service_details(request):
     layout, username, photo, balance, bonus = layout_name(request)
     return render(request, 'Main/Service_details.html', locals())

def User_reviews(request):
     layout, username, photo, balance, bonus = layout_name(request)
     return render(request, 'Main/User_reviews.html', locals())

# def Private_messages(request):
#      layout, username, photo = layout_name(request)
#      return render(request, 'Main/../templates/Profile/Private_messages.html', locals())

def Chat(request):
     layout, username, photo, balance, bonus = layout_name(request)
     return render(request, 'Main/../templates/Profile/Chat.html', locals())
