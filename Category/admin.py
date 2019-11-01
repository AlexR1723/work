from django.contrib import admin
from .models import *
# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

    class Meta:
        model = Category


admin.site.register(Category, CategoryAdmin)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SubCategory._meta.fields]
    list_filter = ['category']
    search_fields = ['name']

    class Meta:
        model = SubCategory


admin.site.register(SubCategory, SubCategoryAdmin)