from django.shortcuts import render


# crates hello world.
def index(request):
    context = dict(
        title = "Hello!",
    )
    return render(request, 'crates/base.html', context)



