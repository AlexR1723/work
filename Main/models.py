from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Comments(models.Model):
    user_id = models.IntegerField(blank=True, null=True, verbose_name="Пользователь")
    text = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Текст отзыва")

    class Meta:
        managed = False
        db_table = 'comments'
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")