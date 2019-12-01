from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from uuslug import slugify
# Create your models here.

class News(models.Model):
    type = models.ForeignKey('NewsType', models.DO_NOTHING, blank=True, null=True, verbose_name="Тип новости")
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    description = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Изображение")
    date = models.DateField(blank=True, null=True, verbose_name="Дата добавления")
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    image_alt = models.CharField(max_length=500, blank=True, null=True)
    slug = models.TextField(blank=True, null=True, verbose_name="Ссылка")

    class Meta:
        managed = False
        db_table = 'news'
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")

    def get_absolute_url(self):
        # return reverse('News_detail', kwargs={'slug': str(self.id)+'-'+self.slug})
        return reverse('News_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            super(News, self).save(*args, **kwargs)
            # id = News.objects.all().order_by('id').reverse()[0].id
            string = str(self.id) + '-' + self.text
        else:
            string = str(self.id) + '-' + self.text
        self.slug = slugify(string)
        super(News, self).save(*args, **kwargs)


class NewsType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование типа")

    class Meta:
        managed = False
        db_table = 'news_type'
        verbose_name = _("Тип новости")
        verbose_name_plural = _("Типы новостей")

    def __str__(self):
        return self.name


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
        city = City.objects.filter(region=self)
        return city


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

    class Meta:
        managed = False
        db_table = 'users'


class UserType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'
