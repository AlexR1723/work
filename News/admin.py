from django.contrib import admin
from .models import *
# Register your models here.

# def translite(name):
#     name=name+'gg'
#     return name

# def translite(self, obj: models.News):
#     link = reverse("admin:module_model_change", args=[obj.model.id])
#     return name

class NewsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NewsType._meta.fields]

    class Meta:
        model = NewsType


admin.site.register(NewsType, NewsTypeAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in News._meta.fields]
    list_filter = ['type']
    exclude = ('slug',)

    class Meta:
        model = News


admin.site.register(News, NewsAdmin)