from django.shortcuts import render

from django.http import HttpResponse
from django.views.generic import View

from cas import BasicCAS

cas = BasicCAS()

class Cas(View):
        def get(self, request, ref):
            filepath = cas.select(ref)

            #  grossly inefficient. Replace with streamer for development, and
            #  X-Sendfile for production.
            with open(filepath,'rb') as f:
                return HttpResponse(f.read())
