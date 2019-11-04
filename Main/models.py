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
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Иконка")

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

    class Meta:
        managed = False
        db_table = 'sub_category'
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")

class Comments(models.Model):
    user_id = models.IntegerField(blank=True, null=True, verbose_name="Пользователь")
    text = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Текст отзыва")

    class Meta:
        managed = False
        db_table = 'comments'
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")


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