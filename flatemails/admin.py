from models import *
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class AlternativeContentInline(admin.StackedInline):
    model = AlternativeContent

class FlatEmailAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('key', 'title', 'from_email', 'to_email', 'content', 'sites')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('template_name',)}),
    )
    list_display = ('key', 'title')
    list_filter = ('sites',)
    search_fields = ('key', 'title')
    inlines = [AlternativeContentInline]
    
admin.site.register(FlatEmail, FlatEmailAdmin)