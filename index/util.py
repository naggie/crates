from PIL import Image
from cas.models import cas
from django.conf import settings
from io import BytesIO

def make_thumbnail_ref(data):
    """
    Makes a thumbnail that is 256x256 (default) fitting the width, truncating
    the height if necessary. Unlike the Image.thumbnail method.

    Will just crop the image square if dimensions are less than 256x256 to
    prevent making the image worse, especially as the responsive web interface
    already scales the image.
    """
    original = BytesIO(data)

    im = Image.open(original)

    if im.size[0] < 256:
        # NOTE: cropping past the image boundary produces a larger image with
        # black gaps
        im.crop((
            0,
            0,
            im.size[0],
            im.size[0],
        ))
    else:
        im.thumbnail((
            settings.THUMBNAIL_WIDTH,
            im.size[1]
        ),resample=Image.LANCZOS)

        im = im.crop((
            0,
            0,
            settings.THUMBNAIL_WIDTH,
            settings.THUMBNAIL_WIDTH
        ))

    # emulate a file again as tobytes doesn't play well with anything other than raw
    thumbnail = BytesIO()
    im.save(thumbnail,'jpeg',encoder_name='jpeg',quality=90,optimize=True)

    return cas.insert_blob(thumbnail.getvalue())




