from django.contrib import admin

from django.contrib import admin
from models import Peer

@admin.register(Peer)
class PeerAdmin(admin.ModelAdmin):
    list_display = ('alias','host','objects_common','object_count')
    search_fields = list_display
