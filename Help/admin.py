from django.contrib import admin
from .models import *

# Register your models here.
class HelpSubcategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HelpSubcategory._meta.fields]

    class Meta:
        model = HelpSubcategory


admin.site.register(HelpSubcategory, HelpSubcategoryAdmin)



class HelpCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HelpCategory._meta.fields]

    class Meta:
        model = HelpCategory


admin.site.register(HelpCategory, HelpCategoryAdmin)



class HelpImagesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HelpImages._meta.fields]

    class Meta:
        model = HelpImages


admin.site.register(HelpImages, HelpImagesAdmin)