from django.db.models import URLField, GenericIPAddressField, CharField, UUIDField, IntegerField, Model
from uuid import uuid4

class Peer(Model):
    #ip = GenericIPAddressField(help_text="IP address of the host")
    url = URLField(help_text="API url of peer")
    alias = CharField(max_length=64,help_text='name of person or node')

    their_key = UUIDField(unique=True,default=uuid4,help_text="Key to authenticate Peer on this server. Give to peer. May be replaced with cjdns IP based pubkey auth later.")

    your_key = UUIDField(help_text="Key to access peer's API")

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

    def __unicode__(self):
        return self.alias
