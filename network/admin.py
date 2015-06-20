from django.contrib import admin
from django.contrib import admin
from models import CratesUser
from django.contrib.auth.models import Group

# Groups are not used, in favor of per-user flags.
# Crates use case involves just a handful of users.
admin.site.unregister(Group)



@admin.register(CratesUser)
class CratesUserAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','objects_common','object_count','has_api_access','can_upload')
    readonly_fields = ('bytes_inbound','bytes_outbound','object_count','bytes_available','bytes_total','objects_common')
    search_fields = list_display

    # suit tabs: http://django-suit.readthedocs.org/en/latest/form_tabs.html
    # awfully hacky but nice result
    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['username','api_key','has_api_access','can_upload','user_server_url','user_server_api_key'],
        }),
        ('Statistics', {
            'classes': ('suit-tab', 'suit-tab-statistics',),
            'fields': readonly_fields,
        }),
    ]

    suit_form_tabs = (('general', 'General'), ('statistics', 'Statistics'))


