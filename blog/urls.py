from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/drafts/$', views.post_drafts, name='post_drafts'),
    #url(r'^post/create/$', views.post_create, name='post_create'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
  	url(r'^accounts/signup/$', views.signup, name='signup'),
  	url(r'^post/(?P<pk>\d+)/addcomment/$', views.add_comment, name='add_comment'),
  	url(r'^post/(?P<pk>\d+)/comment/(?P<ck>\d+)/removecomment/$', views.remove_comment, name='remove_comment'),
  	url(r'^post/(?P<pk>\d+)/comment/(?P<ck>\d+)/editcomment/$', views.edit_comment, name='edit_comment'),

]