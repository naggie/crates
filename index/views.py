from os import stat
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import FileResponse,HttpResponse
from django.core.serializers import get_serializer
from django.conf import settings
from cas.cas import BasicCAS

from models import AudioFile
from django.contrib.auth.decorators import login_required

# TODO: authentication for Peers via middleware and decorators

class DumpIndex(View):
    '''Streaming JSON serialised dump of entire database.'''
    model = AudioFile

    @login_required
    def get(self,request):
        # yet another example of the many layers of abstraction that django
        # enforces for no real benefit. Hey, Java called. They want their
        # string objects back!
        serialize = get_serializer('json')().serialize
        # N.B. request.dict is a http.QueryDict with multiple possible values
        # for the same key. Change to singular with dict()
        queryset = self.model.objects.filter(**request.GET.dict())

        # TODO: this really needs to be streaming
        response = HttpResponse(content_type="application/json")
        serialize(queryset,stream=response)
        return response

