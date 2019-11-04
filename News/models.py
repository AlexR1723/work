from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.

class News(models.Model):
    type = models.ForeignKey('NewsType', models.DO_NOTHING, blank=True, null=True, verbose_name="Тип новости")
    text = models.CharField(max_length=500, blank=True, null=True, verbose_name="Заголовок")
    description = models.TextField(max_length=5000, blank=True, null=True, verbose_name="Описание")
    image = models.ImageField(upload_to='uploads/', blank=True, null=True, verbose_name="Изображение")
    date = models.DateField(blank=True, null=True, verbose_name="Дата добавления")

    class Meta:
        managed = False
        db_table = 'news'
        verbose_name = _("Новость")
        verbose_name_plural = _("Новости")


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