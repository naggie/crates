from django.contrib import admin
from models import AudioFile

# Monkey patch FTW!
admin.site.site_header = 'Crates server administration'


def cover_art_html(audioFile):
    # TODO: replace this with CAS-powered image field + admin form
    if audioFile.cover_art_ref:
        return r"""
            <img src="/cas/{cover_art_ref}" width="512"/>
        """.format(**audioFile.__dict__).replace('\n','')

def audio_preview_html(audioFile):
    # TODO: replace this with CAS-powered image field + admin form
    return r"""
        <audio src="/cas/{ref}" controls preload="auto"></audio>
    """.format(**audioFile.__dict__).replace('\n','')

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title','album','artist','bitrate_kbps','genre','year')
    search_fields = list_display

    def cover_art(self,audioFile): return cover_art_html(audioFile)
    cover_art.allow_tags = True

    def preview_audio(self,audioFile): return audio_preview_html(audioFile)
    preview_audio.allow_tags = True

    readonly_fields = ('cover_art','preview_audio','hits','ref')

    # TODO subclass readonly modeladmin
    #def get_readonly_fields(self, request, obj=None):
    #        return [f.name for f in self.model._meta.fields]

    # add AudioFiles programatically only, via from_file() classmethod
    def has_add_permission(self, request): return False
