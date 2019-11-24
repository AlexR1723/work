from django.contrib import admin
from .models import *

# Register your models here.


class AboutAdmin(admin.ModelAdmin):
    list_display = [field.name for field in About._meta.fields]

    class Meta:
        model = About


admin.site.register(About, AboutAdmin)
