from django.urls import path

from .views import *

app_name = 'posts'

urlpatterns = [
    path('', post_home, name='home'),
    path('detail/', post_detail, name='detail'),
]