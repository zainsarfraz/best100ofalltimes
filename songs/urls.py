
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('',songsIndex,name='songsIndex'),
    path('search',search,name='search'),
    path('vote',vote,name='vote'),
]
