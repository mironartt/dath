from django.contrib import admin
# from .models.globals import Images
from django.utils.html import format_html


# @admin.register(BlogPost)
# class BlogPostAdmin(admin.ModelAdmin):
#
#     save_on_top = True
#     list_display = ['id', 'show_image', 'main_image', 'title', 'short_description', 'get_short_body', 'availavled',]
#     readonly_fields = ['show_image', ]
#
#     def show_image(self, obj):
#         return format_html('<a href="{0}" target="_blank"><img src="{0}" width="150px" /></a>'.format(obj.main_image.image.url))
#
#     def get_short_body(self, obj):
#         return obj.body[:800] + '  ......'
#
#     show_image.short_description = 'Главное изображение'
#     get_short_body.short_description = 'Тело поста'

