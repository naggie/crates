from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^albums$', views.AlbumsView.as_view(), name='index'),
    url(r'^audiofiles$', views.AudioFilesView.as_view(), name='index'),
]
