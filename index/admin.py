from django.contrib import admin
from models import AudioFile,Album
import humanize

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
        <audio src="/cas/{ref}" controls preload="none"></audio>
    """.format(**audioFile.__dict__).replace('\n','')

class AudioFileInline(admin.TabularInline):
    model = AudioFile
    extra = 0

    # removes 'Add another'
    max_num = 0

    fields = ('title','album','artist','preview_audio','bitrate_kbps','genre','year')
    readonly_fields = fields
    show_change_link = True

    def preview_audio(self,audioFile):
        return audio_preview_html(audioFile)
    preview_audio.allow_tags = True


@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('title','album','artist','bitrate_kbps','genre','year')
    search_fields = list_display
    raw_id_fields = 'deprecated_by','album_object'

    def cover_art(self,audioFile): return cover_art_html(audioFile)
    cover_art.allow_tags = True

    def preview_audio(self,audioFile):
        return audio_preview_html(audioFile)
    preview_audio.allow_tags = True

    readonly_fields = ('cover_art','preview_audio','hits','ref','filesize','length')

    def filesize(self,audioFile):
        return humanize.naturalsize(audioFile.size)


    # TODO subclass readonly modeladmin
    #def get_readonly_fields(self, request, obj=None):
    #        return [f.name for f in self.model._meta.fields]

    # add AudioFiles programatically only, via from_file() classmethod
    def has_add_permission(self, request):
        return False

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name','artist','mbid',)
    inlines = AudioFileInline,
