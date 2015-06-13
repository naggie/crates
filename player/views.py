from django.shortcuts import render


# crates hello world.
def index(request):
    context = {}
    return render(request, 'crates/base.html', context)



