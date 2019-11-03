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
        verbose_name = _("Слайдер")
        verbose_name_plural = _("Слайды")



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
        print(sub)
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