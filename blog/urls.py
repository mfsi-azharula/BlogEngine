"""
    @author:Mindfire
    @dateCreated:
    url container file  which contaiins all the url variables of blog apps.
"""

from django.conf.urls.defaults import *
from blog.models import *
from django.core.urlresolvers import reverse
from blog import views

urlpatterns = patterns('',

   url(r"^(\d+)/$", views.post, name='post'),
   url(r"^add_comment/(\d+)/$", views.add_comment, name='add_comment'),
   url(r"^delete_comment/(\d+)/$", views.delete_comment, name='delete_comment'),
   url(r"^delete_comment/(\d+)/(\d+)/$", views.delete_comment, name='delete_comment'),
   url(r"^month/(\d+)/(\d+)/$", "month"),
   url(r'^$', views.main, name='main'),
)
