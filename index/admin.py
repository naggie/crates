from django.contrib import admin
from models import AudioFile

# Monkey patch FTW!
admin.site.site_header = 'Crates server administration'


def cover_art_html(audioFile):
    # TODO: replace this with CAS-powered image field + admin form
    if audioFile.cover_art_ref:
        return r"""
            <img src="/cas/{cover_art_ref}" height="512"/>
        """.format(**audioFile.__dict__)

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title','album','artist','bitrate_kbps','genre','year')
    search_fields = list_display

    def cover_art(self,audioFile):
        return cover_art_html(audioFile)

    cover_art.allow_tags = True

    readonly_fields = ('cover_art',)

    # add AudioFiles programatically only, via from_file() classmethod
    def has_add_permission(self, request): return False
