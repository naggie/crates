from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),


    # TODO move this into a index app with an automatic whitelist
    url(r'^index/Album$', views.AlbumsView.as_view()),
    url(r'^index/AudioFiles$', views.AudioFilesView.as_view()),
]
