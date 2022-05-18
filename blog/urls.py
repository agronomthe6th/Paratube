from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('posts/', PostList.as_view(), name='posts'),
    path('read/<slug:slug>/', PostDetail.as_view(), name='post'),
]
