from django.db.models import URLField, GenericIPAddressField, CharField, UUIDField, IntegerField, Model, BooleanField,OneToOneField
from django.contrib.auth.models import User
from uuid import uuid4

class Profile(Model):
    '''
    A Crates user has access to the media on this server. The user may also be
    allowed to connect his/her own crates server to this one.

    This is a one-to-one relationship used to extend the existing user model without much effort.
    '''

    user = OneToOneField(User)

    has_api_access = BooleanField(default=False, help_text="Can this user crawl this server from their crates server?")
    api_key = UUIDField(
        unique=True,
        default=uuid4,
        help_text="Key used to identify user's crates server",
    )

    can_upload = BooleanField(
        default=False,
        help_text="Is the user allowed to push files to this crates server? Not implemented yet."
    )

    # some stats... (need revising and improvement)
    bytes_inbound = IntegerField(default=0,editable=False)
    bytes_outbound = IntegerField(default=0,editable=False)
    object_count = IntegerField(default=0,editable=False)

    bytes_available = IntegerField(default=0,editable=False)
    bytes_total = IntegerField(default=0,editable=False)

    objects_common = IntegerField(
        default=0,
        editable=False,
        help_text="Mutual CAS objects. Good for data backup"
    )
