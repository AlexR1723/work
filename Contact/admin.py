from django.contrib import admin
from .models import *
# Register your models here.


class ContactAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]
    list_filter = ['type']

    class Meta:
        model = Contact


admin.site.register(Contact, ContactAdmin)


# class ContactTypeAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in ContactType._meta.fields]
#
#     class Meta:
#         model = ContactType
#
#
# admin.site.register(ContactType, ContactTypeAdmin)