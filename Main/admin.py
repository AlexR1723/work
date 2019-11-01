from django.contrib import admin
from .models import *
# Register your models here.


class CommentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comments._meta.fields]

    class Meta:
        model = Comments


admin.site.register(Comments, CommentsAdmin)