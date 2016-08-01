from django.conf.urls import url
from . import views 

urlpatterns = [
    #url(r'^', views.index, name='index'),
    url(r'^$', views.post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<id>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^update/$', views.post_update, name='post_update'),
    url(r'^delete/$', views.post_delete, name='post_delete'),

]
