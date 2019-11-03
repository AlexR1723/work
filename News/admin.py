from django.contrib import admin
from .models import *
# Register your models here.


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NewsType._meta.fields]

    class Meta:
        model = NewsType


admin.site.register(NewsType, NewsTypeAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in News._meta.fields]
    list_filter = ['type']

    class Meta:
        model = News


admin.site.register(News, NewsAdmin)