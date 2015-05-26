from os import stat
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import FileResponse
from cas import BasicCAS

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

