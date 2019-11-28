from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
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


class Link(models.Model):
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="Иконка")

    class Meta:
        managed = False
        db_table = 'link'
        verbose_name = _("Ссылка")
        verbose_name_plural = _("Ссылки")


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