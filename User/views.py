# from django.shortcuts import render
#
# from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
#
# import json
# import random
# from .models import *
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.hashers import check_password,make_password
#
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from django.db import transaction
# from django.conf import settings
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives, EmailMessage
# from django.template.loader import render_to_string
# from django.urls import reverse
#
# def change_password(request):
#     old=request.GET.get('old')
#     new1=request.GET.get('new1')
#     new2=request.GET.get('new2')
#     # id=request.session['user_id']
#     user_id=29
#     # db_pas = AuthUser.objects.filter(id=user_id)
#     # db_pass=AuthUser.objects.get(id=request.session['user_id'])
#     db_pass='grinya22041982'
#     check=check_password(old, db_pass)
#     if(check == True):
#         new1=make_password(new1)
#         new2=make_password(new2)
#         if new1==new2:
#             AuthUser.objects.get(id=user_id).update(password=new1)
#             return HttpResponse(json.dumps('Пароли изменён'))
#         else:
#             return HttpResponse(json.dumps('Пароли не совпадают'))
#     else:
#         return HttpResponse(json.dumps('Старый пароль неверный'))
#     # pas1 = request.GET.get("pas1")
#     # pas2 = request.GET.get("pas2")
#     # pas3 = request.GET.get("pas3")
#     # # id=request.session['userid']
#     # # db_pas=AuthUser.objects.filter(id=request.session['userid'])
#     # pas4 = AuthUser.objects.filter(id=request.session['userid'])[0].password
#     # us = check_password(pas1, pas4)
#     #
#     # # print(us)
#     # if (us == True):
#     #     nw = make_password(pas3)
#     #     print('1 if')
#     #     if (pas2 == pas3):
#     #         AuthUser.objects.filter(id=request.session['userid']).update(password=nw)
#     #         return HttpResponse(json.dumps({'data': 'Пароль изменён'}))
#     #     else:
#     #         return HttpResponse(json.dumps({'data': 'Пароли не совпадают'}))
#     # else:
#     #     return HttpResponse(json.dumps({'data': 'Старый пароль неверный'}))
#     # return HttpResponse(json.dumps('bad'))
