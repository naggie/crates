from os import stat
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import FileResponse,HttpResponse
from django.core.serializers import get_serializer
from cas import BasicCAS

from models import AudioFile

# TODO: authentication for Peers via middleware and decorators


cas = BasicCAS()

class Cas(View):
    # TODO Subclass this to include actual filepath and better name. Based on audioFile.map
    def get(self, request, ref):
        '''
        Serve a file from the CAS. Not scalable, as it ties up an entire
        UWSGI worker. However, it's better than simply f.read()ing a file into
        a HttpResponse which loads the entire file into memory.

        Instead, FileResponse (a subclass of StreamingHttpResponse) streams the
        file in chunks. For a big ubuntu ISO, the memory usage went down from
        around 1000MB to just 30MB. This was measured using the memory_profiler
        module.


        For (scalable) production usage, an X-Sendfile mechanism is required
        and will be implemented soon.
        '''
        filepath = cas.select(ref)

        response = FileResponse(
            open(filepath,'rb'),
            content_type="application/octet-stream"
        )

        response['Content-Length'] = stat(filepath).st_size
        return response

class DumpIndex(View):
    '''Streaming JSON serialised dump of entire database.'''
    model = AudioFile

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




