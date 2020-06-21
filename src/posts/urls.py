from django.urls import path, re_path

from .views import *

app_name = 'posts'

urlpatterns = [
    path('', post_home, name='home'),
    re_path(r'(?P<id>\d+)/$', post_detail, name='detail'),
    path('new/', post_create, name='create'),
    re_path(r'(?P<id>\d+)/edit/$', post_update, name='update'),
    re_path(r'(?P<id>\d+)/delete/$', post_delete, name='delete'),
]