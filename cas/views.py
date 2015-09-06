from os import stat
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.http import FileResponse,HttpResponse
from django.conf import settings
from cas import BasicCAS
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import re
from mimetypes import guess_type

# TODO: authentication for Peers via middleware for API

# TODO: http://stackoverflow.com/questions/6069070/how-to-use-permission-required-decorators-on-django-class-based-views
# change to mixin


cas = BasicCAS()

class Cas(View):
    # TODO Subclass this to include actual filepath and better name. Based on audioFile.map

    # require login hack, allowing the login_required decorator able to be used for class based views
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(Cas, self).dispatch(*args, **kwargs)

    def get(self, request, ref, ext='.bin'):
        '''
        Serve a file from the CAS. Not scalable, as it ties up an entire
        UWSGI worker. However, it's better than simply f.read()ing a file into
        a HttpResponse which loads the entire file into memory.

        Instead, FileResponse (a subclass of StreamingHttpResponse) streams the
        file in chunks. For a big ubuntu ISO, the memory usage went down from
        around 1000MB to just 30MB. This was measured using the memory_profiler
        module.


        For (scalable) production usage, an X-Sendfile mechanism is required.
        Beware, assumes ref is a valid cas ref from the URL pattern.
        '''

        # append an extension to the URL if you know it for convenience.
        mimetype = guess_type('foo.%s' % ext,strict=False)[0]

        if settings.X_SENDFILE:
            response = HttpResponse()
            # This resource is immutable by definition.
            # To mark a response as "never expires," an origin server sends an
            # Expires date approximately one year from the time the response is
            # sent. HTTP/1.1 servers SHOULD NOT send Expires dates more than
            # one year in the future.
            response['Cache-Control'] = 'max-age=31556926'
            response['X-Accel-Redirect'] =  '/accel_cas/'+ref[:2]+'/'+ref[2:]+'.bin'
            if mimetype: response['Content-Type'] = mimetype
            return response


        filepath = cas.select(ref)
        file_obj = open(filepath,'rb')
        start = 0

        # Deal with HTTP/1.1 Range request. Note that if X_SENDFILE is used,
        # nginx will do this automatically.
        # For now just support a 'from.' If a 'to' is specified, give a 416.
        # https://en.wikipedia.org/wiki/Byte_serving
        if 'HTTP_RANGE' in request.META:
            try:
                r = request.META['HTTP_RANGE']
                start, stop = re.findall(r'^bytes=([0-9]+)-([0-9]+)?$',r)[0]

                start = int(start)

                if stop:
                    raise IndexError()

            except IndexError:
                # 416 Requested Range Not Satisfiable
                return HttpResponse(status=416)

        file_obj.seek(start)
        response = FileResponse(file_obj)

        # CAS -- by definition does not change -- ever.
        response['Cache-Control'] = 'max-age=31556926'
        if mimetype: response['Content-Type'] = mimetype

        # seeked via range handler above

        # Intestingly, in order for seeking to work not only do you need to
        # support Range requests, you also need to honor the first request as a
        # range request even if the first requested byte is 0!
        # http://stackoverflow.com/questions/8088364/html5-video-will-not-loop
        if 'HTTP_RANGE' not in request.META:
            response.status_code = 200
            response['Content-Length'] = stat(filepath).st_size
        else:
            # 206 Partial content
            response.status_code = 206
            response['Content-Length'] = stat(filepath).st_size - start
            response['Content-Range'] = 'bytes {start}-{end}/{total}'.format(
                start = start,
                end = stat(filepath).st_size - 1,
                total = stat(filepath).st_size
            )

        return response

class EnumerateCas(View):
    # require login hack, allowing the login_required decorator able to be used for class based views
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EnumerateCas, self).dispatch(*args, **kwargs)

    def get(self, request):
        response = FileResponse(
            self._json_generator(),
            content_type="application/json"
        )

        return response

    def _json_generator(self):
        '''Manual JSON generator for streaming'''
        # TODO: could be generalised to be a generator decorator for creating a
        # JSON list out of arbitrary objects (json dump each object)
        generator = cas.enumerate()

        yield '["%s"' % next(generator)

        for ref in generator:
            yield ',\n"%s"' % ref

        yield ']'
