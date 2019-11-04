from django.contrib import admin
from .models import *
# Register your models here.


class CommentsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comments._meta.fields]

    class Meta:
        model = Comments


admin.site.register(Comments, CommentsAdmin)


class FirstSliderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FirstSlider._meta.fields]

    class Meta:
        model = FirstSlider


admin.site.register(FirstSlider, FirstSliderAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Link._meta.fields]

    class Meta:
        model = Link


admin.site.register(Link, LinkAdmin)


class OrderServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OrderService._meta.fields]

    class Meta:
        model = OrderService


admin.site.register(OrderService, OrderServiceAdmin)