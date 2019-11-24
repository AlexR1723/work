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