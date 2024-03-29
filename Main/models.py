from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class FirstSlider(models.Model):
    text = models.CharField(max_length=100, blank=True, null=True, verbose_name="Заголовок")
    description = models.CharField(max_length=500, blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        managed = False
        db_table = 'first_slider'
        verbose_name = _("Слайд")
        verbose_name_plural = _("Слайдер")



class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование категории")
    image = models.ImageField(upload_to='uploads/category/', blank=True, null=True, verbose_name="Иконка")
    text = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name

    def first_five(self):
        sub=SubCategory.objects.all().filter(category=self)[:5]
        return sub

    def rest(self):
        sub=SubCategory.objects.all().filter(category=self)[5:]
        return sub


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование")
    image = models.ImageField(upload_to='uploads/subcategory/', blank=True, null=True, verbose_name="Картинка")
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_category'
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")

    def task_count(self):
        count=UserTask.objects.all().filter(subcategory=self).filter(task_status__name='В поиске').count()
        return count



class Link(models.Model):
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="Иконка")

    class Meta:
        managed = False
        db_table = 'link'
        verbose_name = _("Ссылка")
        verbose_name_plural = _("Ссылки")


class Contact(models.Model):
    type = models.ForeignKey('ContactType', models.DO_NOTHING, blank=True, null=True, verbose_name="Тип контакта")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'contact'
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")


class ContactType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'contact_type'
        verbose_name = _("Тип контакта")
        verbose_name_plural = _("Типы контактов")

    def __str__(self):
        return self.name


class OrderService(models.Model):
    text = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'order_service'
        verbose_name = _("Текст")
        verbose_name_plural = _("Текст 'Как заказать услугу'")


class WhyWe(models.Model):
    header = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Текст")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Картинка")
    left = models.BooleanField(blank=True, null=True, default=True, verbose_name="Картинка слева?")

    class Meta:
        managed = False
        db_table = 'why_we'
        verbose_name = _("Текст")
        verbose_name_plural = _("Текст 'Почему мы'")



class BecomePerformer(models.Model):
    text = models.CharField(max_length=5000, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'become_performer'
        verbose_name = _("Текст")
        verbose_name_plural = _("Текст 'Как стать исполнителем'")


class WhatSafe(models.Model):
    text = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'what_safe'
        verbose_name = _("Текст")
        verbose_name_plural = _("Текст 'Что такое безопасная сделка'")


class BenefitsSafe(models.Model):
    header = models.CharField(max_length=200, blank=True, null=True, verbose_name="Заголовок")
    text = models.TextField(max_length=500, blank=True, null=True, verbose_name="Текст")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        managed = False
        db_table = 'benefits_safe'
        verbose_name = _("Преимущества безопасной сделки")
        verbose_name_plural = _("Преимущество безопасной сделки")


class PrivacyRules(models.Model):
    # number = models.IntegerField(blank=True, null=False, verbose_name="Порядковый номер")
    number = models.IntegerField(verbose_name="Порядковый номер")
    header = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    text = models.TextField(blank=True, null=True, verbose_name="Текст",help_text="Подпункты разделять двойным переносом строки")

    class Meta:
        managed = False
        db_table = 'privacy_rules'
        verbose_name = _("Правило конфиденциальности")
        verbose_name_plural = _("Правила конфиденциальности")


class ProjectRules(models.Model):
    number = models.IntegerField(verbose_name="Порядковый номер")
    header = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    text = models.TextField(blank=True, null=True, verbose_name="Текст",
                            help_text="Подпункты разделять двойным переносом строки")

    class Meta:
        managed = False
        db_table = 'project_rules'
        verbose_name = _("Правило проекта")
        verbose_name_plural = _("Правила проекта")


class PublicOffer(models.Model):
    number = models.IntegerField(verbose_name="Порядковый номер")
    header = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    text = models.TextField(blank=True, null=True, verbose_name="Текст",
                            help_text="Подпункты разделять двойным переносом строки")

    class Meta:
        managed = False
        db_table = 'public_offer'
        verbose_name = _("Публичная оферта")
        verbose_name_plural = _("Публичные оферта")


class City(models.Model):
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True, verbose_name="Регион")
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = _("Город")
        verbose_name_plural = _("Города")


class Region(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'region'
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")

    def cities(self):
        city=City.objects.filter(region=self)
        return city

    def __str__(self):
        return self.name


class HelpCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Наименование")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Картинка")

    class Meta:
        managed = False
        db_table = 'help_category'
        verbose_name = _("Категория вопроса")
        verbose_name_plural = _("Категории вопросов")

    def __str__(self):
        return self.name

    def questions(self):
        quest=HelpSubcategory.objects.filter(help_category_id=self)
        return quest


class HelpSubcategory(models.Model):
    help_category = models.ForeignKey(HelpCategory, models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Текст вопроса")

    class Meta:
        managed = False
        db_table = 'help_subcategory'
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


    def get_user(self):
        user=Users.objects.get(auth_user=self)
        return user

    def get_comment_count(self):
        all_task = UserComment.objects.filter(user=self).count()
        return all_task

    def get_percent(self):
        all_task = UserComment.objects.filter(user=self).count()
        successful_task = UserComment.objects.filter(user=self).filter(quality__gte=4).filter(
            politeness__gte=4).filter(punctuality__gte=4).count()
        com_percent = 0
        if all_task > 0:
            com_percent = int((successful_task * 100) / all_task)
        return com_percent





class Comments(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'



class Gender(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class Users(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('UserType', models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    gender = models.ForeignKey(Gender, models.DO_NOTHING, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    about_me = models.CharField(max_length=5000, blank=True, null=True, default=" ")
    get_new_order = models.BooleanField(blank=True, null=True)
    get_notice_status = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/users/', max_length=100, blank=True, null=True)
    verify_phone = models.BooleanField(blank=True, null=True)
    verify_passport = models.BooleanField(blank=True, null=True)
    passport_photo = models.ImageField(upload_to='uploads/users/', max_length=500, blank=True, null=True)
    verify_date = models.DateField(blank=True, null=True)
    passport_num_ser = models.CharField(max_length=50, blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    bonus_balance = models.IntegerField(blank=True, null=True)
    frozen_balance = models.IntegerField(blank=True, null=True)
    last_online = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UserTaskStatus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_status'


class UserAdvert(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    photo_main = models.ImageField(upload_to='uploads/advert/',max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    count_offer = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert'


class UserOffer(models.Model):
    user_id_customer = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='user_id_customer', blank=True, null=True)
    advert = models.ForeignKey('UserAdvert', models.DO_NOTHING, blank=True, null=True)
    is_accept = models.BooleanField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_offer'



class UserTask(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)
    photo_main = models.ImageField(upload_to='uploads/task/', max_length=500, blank=True, null=True)
    task_status = models.ForeignKey('UserTaskStatus', models.DO_NOTHING, db_column='task_status', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    exec = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True,related_name='exec_id')
    date_add = models.DateField(blank=True, null=True)
    rezult_text = models.CharField(max_length=5000, blank=True, null=True)
    exec_finish = models.BooleanField(blank=True, null=True)
    offer = models.ForeignKey(UserOffer, models.DO_NOTHING, blank=True, null=True)
    is_pro = models.BooleanField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task'



class UserType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'



class UserPro(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_pro'



class UserComment(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    task = models.ForeignKey('UserTask', models.DO_NOTHING, blank=True, null=True)
    customer = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True, related_name='customer_id')
    date = models.DateField(blank=True, null=True)
    quality = models.IntegerField(blank=True, null=True)
    politeness = models.IntegerField(blank=True, null=True)
    punctuality = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_comment'


class Bonuses(models.Model):
    backend_name = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bonuses'





class UserBonuses(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    bonus = models.ForeignKey(Bonuses, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_bonuses'



class Awards_model(models.Model):
    backend_name = models.TextField(blank=True, null=True)
    name = models.TextField(blank=True, null=True)
    tooltip = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'awards'



class UserAwards(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    awards = models.ForeignKey('Awards_model', models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_awards'


class Notifications(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    is_checked = models.BooleanField(blank=True, null=True)
    date_public = models.DateTimeField(blank=True, null=True)
    is_show = models.BooleanField(blank=True, null=True)
    for_executor = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'

