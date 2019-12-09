from django.contrib import admin
from core.models import User, Cards
from django.utils.html import format_html


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ['id', 'login', 'cart_number', 'cart_type', 'passport_series', 'place_birth', 'refer', 'show_image',]
    readonly_fields = ['show_image', ]

    def show_image(self, obj):
        return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150px" /></a>'.format(obj.image.url)) if obj.image else '-'
    show_image.short_description = 'Главное изображение'


@admin.register(Cards)
class CardsAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ['id', 'name', 'offer_profit', 'binnary_profit', 'is_active',]



