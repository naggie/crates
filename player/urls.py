from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),


    # TODO move this into a index app with an automatic whitelist
    url(r'^albums', views.AlbumsView.as_view()),
    url(r'^audiofiles$', views.AudioFilesView.as_view()),
]
