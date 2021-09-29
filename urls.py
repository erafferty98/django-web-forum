from django.urls import path, include
from . import views
from django.conf import settings
import oauth2_provider.views as oauth2_views
from rest_framework import renderers

app_name = 'posts'

urlpatterns = [
    path('posts/', views.PostViewSet.as_view({'get': 'list','post': 'create','put': 'update'}), name='posts'),
    path('posts/<int:pk>/', views.PostViewSet.as_view({'put':'update','patch': 'partial_update','get': 'list','post': 'create','put': 'update'}),name='details'),
]