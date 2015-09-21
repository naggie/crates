'''
The idea here is this is a semi-transparent ORM gateway such that queries can
be built in a GET request. I'll see what can be factorised into a class. So
far, the JSON list streaming system has been, and the query system will be.
What remains is a flatten (to serialise) method for classes). Time, will tell.

TODO make a module from this, whatever it becomes


Could specify reduction function here, also...

'''
import json
from copy import copy

from index.models import Album,AudioFile

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.http import FileResponse,HttpResponse
from django.db.models import Q


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


# TODO share this with CAS
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


class StreamingJsonObjectView(StreamingJsonView):
    '''Streams & serialises objects by a queryset produced from the GET request.
    define reduce to decide what is serialised or to enable serialisation.

    The idea is general endpoints can be used instead of creating lots of
    specific endpoints.

    May or may not work -- might want to extend with explicit query method.
    '''
    # how many items per page?
    stride = 100

    @staticmethod
    def reduce(obj):
        'Basic reducer, should work on basic objects'
        o = copy(obj.__dict__)
        # remote things that are not required,
        # convert things that are not JSON serialisable
        del o['_state']

        return o

    def enumerate(self):
        qs = self.model.objects

        # TODO evaluate this from a security/performance perspective
        query = self.request.GET.dict()

        try:
            page = query.pop('page')
            page = int(page)
        except KeyError,ValueError:
            page = 0

        # magic key in query
        if 'order_by' in query:
            qs = qs.order_by( query.pop('order_by') )

        if 'operator' in query:
            operator = query.pop('operator')
        else:
            operator = 'AND'

        if operator not in ('OR','AND'):
            raise ValueError('Invalid operator: OR/AND only')

        if (operator == "AND"):
            qs = qs.filter(**query)
        else:
            # build a Q object match (how contrived, although generally
            # speaking swithing |= with &= would accomplish the above)
            q = Q()

            for k,v in query.items():
                q |= Q(**{k:v})

            qs = qs.filter(q)

        s = self.stride
        for obj in qs[page*s:page*s+s]:
            yield self.reduce(obj)


class AlbumsView(LoginRequiredMixin,StreamingJsonObjectView):
    model = Album

    # albums definitions are small
    stride = 300

class AudioFilesView(LoginRequiredMixin,StreamingJsonObjectView):
    model = AudioFile

    @staticmethod
    def reduce(obj):
        o = copy(obj.__dict__)
        # remote things that are not required,
        # convert things that are not JSON serialisable
        del o['type']
        del o['added']
        del o['_state']

        return o
