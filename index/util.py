from PIL import Image
from cas.models import cas
from django.conf import settings
from io import BytesIO

# don't worry, I'm not using this for anything important
from hashlib import md5

from kmeans import colorz


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
    colour = colorz(im)[0]

    # TODO store this separately for placeholder on web. Random if no image.

    # create a substrate to paste on to with the dominant colour
    substrate = Image.new('RGB',(WIDTH,WIDTH),colour)

    # paste in middle if short, or truncate bottom if tall
    if im.size[1] < WIDTH:
        offset = (WIDTH - im.size[1])/2
    else:
        offset = 0

    substrate.paste(im,(0,offset))

    # emulate a file again as tobytes doesn't play well with anything other than raw
    outdata = BytesIO()
    substrate.save(outdata,'jpeg',encoder_name='jpeg',quality=90,optimize=True)

    return cas.insert_blob(outdata.getvalue()), colour



def deterministic_colour(*args):
    m = md5()

    for arg in args:
        arg = str(arg)
        m.update(arg)

    return '#'+m.hexdigest()[:6]

def find_APIC_frame_data(mp3):
    """
    Iterate through ID3 frames in an MP3 object looking for the most likely
    candidate for a front cover
    """
    for key in mp3:
        frame = mp3[key]
        if frame.FrameID == 'APIC':
            return frame.data

