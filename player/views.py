import json

from index.models import Album

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import FileResponse,HttpResponse



# crates hello world.
@login_required
def index(request):
    context = dict(
        title = "Hello!",
    )
    return render(request, 'crates/index.html', context)

# TODO: these parent classes belong in a separate module
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class StreamingJsonView(View):
    def get(self, request):
        response = FileResponse(
            self._json_generator(),
            content_type="application/json"
        )

        return response

    def enumerate():
        'A generator of serialisable structures'
        raise NotImplementedError('Implement this in subclass')

    @staticmethod
    def _json_gen_wrapper(gen):
        for item in gen:
            yield json.dumps(item)

    def _json_generator(self):
        '''Manual JSON generator for streaming'''
        # JSON list out of arbitrary objects (json dump each object)
        gen = self.enumerate()

        gen = self._json_gen_wrapper(gen)

        try:
            yield '[%s' % next(gen)

            for ref in gen:
                yield ',\n%s' % ref

            yield ']'
        except StopIteration:
            yield '[]'

# TODO this is quite generic already, so could merge it into above
class Albums(LoginRequiredMixin,StreamingJsonView):
    def enumerate(self):
        qs = Album.objects

        qs = qs.exclude(cover_art_ref__isnull=True)

        #if 'startswith' in self.request.GET:
        #    qs = qs.filter(name__startswith=self.request.GET['startswith'])

        # TODO evaluate this from a security/performance perspective
        qs = qs.filter(**self.request.GET.dict())


        for album in qs[:100]:
            # TODO filter out _state (etc)
            #yield album.__dict__
            yield {k:v for (k,v) in album.__dict__.iteritems() if not k.startswith('_')}
