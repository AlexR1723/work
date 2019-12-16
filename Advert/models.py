from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class AboutType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование блока")

    class Meta:
        managed = False
        db_table = 'about_type'
        verbose_name = _("Блоки")
        verbose_name_plural = _("Блок 'О нас'")

    def __str__(self):
        return self.name


class About(models.Model):
    type = models.ForeignKey('AboutType', models.DO_NOTHING, blank=True, null=True, verbose_name="Блок")
    text = models.CharField(max_length=5000, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'about'
        verbose_name = _("Текст")
        verbose_name_plural = _("Текст 'О нас'")



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


class Region(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'region'
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")


class City(models.Model):
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True, verbose_name="Регион")
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = _("Город")
        verbose_name_plural = _("Города")

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


class Gender(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_category'


class Users(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('UserType', models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    gender = models.ForeignKey(Gender, models.DO_NOTHING, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    about_me = models.CharField(max_length=5000, blank=True, null=True)
    get_new_order = models.BooleanField(blank=True, null=True)
    get_notice_status = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/users/', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UserType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'

class UserAdvert(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    photo_main = models.ImageField(upload_to='uploads/advert/',max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert'


class UserAdvertPhoto(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    advert = models.ForeignKey(UserAdvert, models.DO_NOTHING, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/advert/',max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert_photo'

