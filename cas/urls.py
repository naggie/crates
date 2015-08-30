from django.conf.urls import url

from views import Cas,EnumerateCas

urlpatterns = [
    url(r'(?P<ref>[0-9a-f]{64})(?P<ext>\..+$)?',Cas.as_view(), name='cas'),
    url(r'$',EnumerateCas.as_view(), name='cas_dump'),
]
