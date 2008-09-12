from models import *
from django.contrib import admin
from simplecart.orders import SHOP_ADMIN_SITE

class FlatEmailAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('key', 'title', 'from_email', 'to_email', 'content', 'sites')}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('template_name',)}),
    )
    list_display = ('key', 'title')
    list_filter = ('sites',)
    search_fields = ('key', 'title')
    
SHOP_ADMIN_SITE.register(FlatEmail, FlatEmailAdmin)