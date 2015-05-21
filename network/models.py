from django.db.models import URLField, GenericIPAddressField, CharField, UUIDField, IntegerField, Model
from uuid import uuid4

class Peer(Model):
    'A peer to connect to. Peer 0 is you.'
    host = GenericIPAddressField(help_text="IP address of the host")
    url = URLField(help_text="API url of field")
    alias = CharField(max_length=64,help_text='name of person or node')

    key = UUIDField(primary_key=True, default=uuid4,help_text="secret key to allow API access to peer")

    # some stats...
    bytes_inbound = IntegerField()
    bytes_outbound = IntegerField()
    object_count = IntegerField()

    bytes_available = IntegerField()
    bytes_total = IntegerField()

    objects_common = IntegerField(help_text="Mutual CAS objects. Good for data backup")
