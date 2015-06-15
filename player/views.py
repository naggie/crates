from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# crates hello world.
@login_required
def index(request):
    context = dict(
        title = "Hello!",
    )
    return render(request, 'crates/index.html', context)



