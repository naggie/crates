from __future__ import division
from PIL import Image
from cas.models import cas
from django.conf import settings
from io import BytesIO

from zlib import adler32
from colorsys import hsv_to_rgb

from kmeans import colorz,rtoh

from mutagen.mp3 import MP3 as _MP3,HeaderNotFoundError


def make_thumbnail_ref(data):
    """
    Makes a thumbnail that is 256x256 (default) fitting the width, truncating
    the height if necessary. Unlike the Image.thumbnail method.

    Will just crop the image square if dimensions are less than 256x256 to
    prevent making the image worse, especially as the responsive web interface
    already scales the image.
    """
    im = Image.open(BytesIO(data))

    if im.size[0] > settings.THUMBNAIL_WIDTH:
        WIDTH = settings.THUMBNAIL_WIDTH
    else:
        WIDTH = im.size[0]


    # scale width
    im.thumbnail((
        WIDTH,
        im.size[1]
    ),resample=Image.LANCZOS)

    # chop height
    im = im.crop((
        0,
        0,
        WIDTH,
        im.size[1],
    ))

    # find the dominant colour (k-grouping)
    try:
        colour = colorz(im)[0]
    except:
        colour = 0,0,0

    # TODO store this separately for placeholder on web. Random if no image.

    # create a substrate to paste on to with the dominant colour
    substrate = Image.new('RGB',(WIDTH,WIDTH),colour)

    # paste in middle if short, or truncate bottom if tall
    if im.size[1] < WIDTH:
        offset = (WIDTH - im.size[1])/2
    else:
        offset = 0

    substrate.paste(im,(0,int(offset)))

    # emulate a file again as tobytes doesn't play well with anything other than raw
    outdata = BytesIO()
    substrate.save(outdata,'jpeg',encoder_name='jpeg',quality=90,optimize=True)

    return cas.insert_blob(outdata.getvalue()), colour



def deterministic_colour(*args):
    '''Produces a weighted deterministic colour'''
    seed = unicode(args)

    # faster than crc32
    hue = adler32(seed) % 256
    sat = 128
    val = 200

    # return CSS RGB hex
    r,g,b = hsv_to_rgb(hue/255,sat/255,val/255)
    return rtoh((r*255,b*255,g*255))



class MP3(_MP3):
    def find_APIC_frame_data(self):
        """
        Iterate through ID3 frames in an MP3 object looking for the most likely
        candidate for a front cover
        """
        for key in self:
            frame = self[key]
            if frame.FrameID == 'APIC':
                return frame.data

    def get_text_frame(self,ids,default=''):
        if isinstance(ids,str): ids = [ids]

        for id in ids:
            if self.has_key(id):
                return self[id][0].capitalize()

        return default

