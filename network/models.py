from django.db.models import URLField, GenericIPAddressField, CharField, UUIDField, IntegerField
from uuid import uuid4

class Peer(models.Model):
    'A peer to connect to. Peer 0 is you.'
    host = models.GenericIPAddressField(help_text="IP address of the host")
    url = models.URLField(help_text="API url of field")
    alias = models.CharField(max_length=64,help_text='name of person or node')

    key = models.UUIDField(primary_key=True, default=uuid4,help_text="secret key to allow API access to peer")

    # some stats...
    bytes_inbound = models.IntegerField()
    bytes_outbound = models.IntegerField()
    object_count = models.IntegerField()

    bytes_available = models.IntegerField()
    bytes_total = models.IntegerField()

    objects_common = models.IntegerField(help_text="Mutual CAS objects. Good for data backup")
