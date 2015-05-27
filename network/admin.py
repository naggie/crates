from django.contrib import admin

from django.contrib import admin
from models import Peer

@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    list_display = ('alias','host','objects_common','object_count')
    readonly_fields = ('bytes_inbound','bytes_outbound','object_count','bytes_available','bytes_total','objects_common')
    search_fields = list_display

    # suit tabs: http://django-suit.readthedocs.org/en/latest/form_tabs.html
    # awfully hacky but nice result
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['alias','url','host','key',],
        }),
        ('Statistics', {
            'classes': ('suit-tab', 'suit-tab-statistics',),
            'fields': readonly_fields,
        }),
    ]

    suit_form_tabs = (('general', 'General'), ('statistics', 'Statistics'))
