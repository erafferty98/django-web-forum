"""piazza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from home.views import PostViewSet, postvote, post_delete, post_update
from home.views import comment_create, comment_update, comment_delete
router = DefaultRouter()
router.register('posts', PostViewSet,basename="posts")
app_name = 'posts'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('authentication/', include('users.urls')),
    path('v1/', include(router.urls,)),
    path('v1/posts/<int:pk>/preference/<int:uservote>/', postvote, name='uservote'),
    path('v1/posts/<int:pk>/update', post_update, name='update'),
    path('v1/posts/<int:pk>/delete', post_delete, name='delete'),
    path('v1/posts/<int:pk>/comment/',comment_create, name='comment-create'),
    path('v1/posts/<int:pk>/comment/<int:id>/update/',comment_update, name='comment-update'),
    path('v1/posts/<int:pk>/comment/<int:id>/delete/',comment_delete, name='comment-delete'),
    
]
