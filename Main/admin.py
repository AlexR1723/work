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


class WhyWeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WhyWe._meta.fields]

    class Meta:
        model = WhyWe


admin.site.register(WhyWe, WhyWeAdmin)


class BecomePerformerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BecomePerformer._meta.fields]

    class Meta:
        model = BecomePerformer


admin.site.register(BecomePerformer, BecomePerformerAdmin)



class WhatSafeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WhatSafe._meta.fields]

    class Meta:
        model = WhatSafe


admin.site.register(WhatSafe, WhatSafeAdmin)



class BenefitsSafeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BenefitsSafe._meta.fields]

    class Meta:
        model = BenefitsSafe


admin.site.register(BenefitsSafe, BenefitsSafeAdmin)







class PrivacyRulesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrivacyRules._meta.fields]

    class Meta:
        model = PrivacyRules


admin.site.register(PrivacyRules, PrivacyRulesAdmin)



class ProjectRulesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProjectRules._meta.fields]

    class Meta:
        model = ProjectRules


admin.site.register(ProjectRules, ProjectRulesAdmin)



class PublicOfferAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PublicOffer._meta.fields]

    class Meta:
        model = PublicOffer


admin.site.register(PublicOffer, PublicOfferAdmin)


class CityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in City._meta.fields]

    class Meta:
        model = City


admin.site.register(City, CityAdmin)


class RegionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Region._meta.fields]

    class Meta:
        model = Region


admin.site.register(Region, RegionAdmin)
