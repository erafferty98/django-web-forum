from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, ListView, DetailView, ArchiveIndexView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import Post, Comment, Vote
from rest_framework import viewsets
from .serializers import PostSerializer,CommentSerializer 
from .forms import CommentForm, PostForm, PostUpdateForm, CommentUpdateForm
from datetime import datetime
from .filters import PostFilter
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth.models import User
from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework import status
from rest_framework.decorators import action, renderer_classes


class PostViewSet(viewsets.ViewSet):


    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'patch':
            permission_classes = [IsAuthenticated]
        elif self.action == 'delete':
            permission_classes = [IsAuthenticated]
        else: 
            permission_classes = [IsAuthenticatedOrReadOnly]

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        Returns the list of posts for the homepage.
        """
        if request.accepted_renderer.format == 'html':
            #create post form
            post_form = PostForm()
            #normal filter
            filterset_class = PostFilter(request.GET, queryset=Post.objects.filter().order_by("-created_at"))
            #additional filter for for likes
            filterset_class2 = PostFilter(request.GET, queryset=Post.objects.filter().order_by("-likes","dislikes"))
            serializer = PostSerializer(many=True)
            context = {'posts': serializer.data,'post_form': post_form,'myFilter': filterset_class,'likesFilter': filterset_class2 }
            return Response(context,template_name = 'posts/index.html')
        elif request.accepted_renderer.format == 'json':
            filterset_class = PostFilter(request.GET, queryset=Post.objects.filter().order_by("-created_at"))
            serializer = PostSerializer(many=True)
            context = {'posts': serializer.data}
            return Response(context)
        return super(PostViewSet, self).list(self, request)


    def create(self, request):
        """
        Create new Post, form above as part of list so can be on same page.
        """
        if request.accepted_renderer.format == 'html':
            Post.objects.create(
                title = request.data["title"],
                topic = request.data["topic"],
                content = request.data["content"],
                created_at = datetime.now(),
                updated_at = datetime.now(),
                created_by = request.user,
                updated_by = request.user,
                expiry_time = request.data["expiry_time"],
                likes = 0,
                dislikes = 0)
            return Response(status=status.HTTP_202_ACCEPTED,template_name = 'returntohome.html')
        elif request.accepted_renderer.format == 'json':
            Post.objects.create(
                title = request.data["title"],
                topic = request.data["topic"],
                content = request.data["content"],
                created_at = datetime.now(),
                updated_at = datetime.now(),
                created_by = request.user,
                updated_by = request.user,
                expiry_time = request.data["expiry_time"],
                likes = 0,
                dislikes = 0)
            return Response(status=status.HTTP_202_ACCEPTED)
        return super(PostViewSet, self).create(self, request)

    def update(self, request, pk):
        pass

    def get(self,request,pk):
        """Post detail with add comment form (in html version) """
        post = get_object_or_404(Post, pk=pk)
        Post.expire_post(post)
        if request.accepted_renderer.format == 'json':
            serializer=PostSerializer(request.user, data=request.data)
            return Response(serializer.data)
        elif request.accepted_renderer.format == 'html':
            comments = Comment.objects.filter(post=post)
            return render(request, 'posts/detail.html', {'posts': post,
                                           'comments': comments})
        return super(PostViewSet, self).get(self, request, pk)

@login_required() #working
@permission_classes([IsAuthenticated])
def post_update(request, pk):
    """
    Update post with update post form and defaul update data
    """
    post = Post.objects.get(pk=pk,status=0)
    update_post = None
    if request.method == 'POST' and request.user == post.created_by:
        post_update_form = PostUpdateForm(request.POST, instance=post)
        if post_update_form.is_valid():
            update_post = post_update_form.save(commit=False)
            update_post.updated_at = datetime.now()
            update_post.updated_by = request.user
            update_post.save()
    else:
        post_update_form = PostUpdateForm()
    return render(request, 'posts/post_update.html', {'posts': post, 'update_post': update_post, 'post_update_form': post_update_form})


@login_required() #working
@permission_classes([IsAuthenticated])
def post_delete(request,pk):
    """Delete Post"""
    post_to_delete = Post.objects.get(pk=pk)
    if request.user == post_to_delete.created_by:
        post_to_delete.delete()
        return render(request, 'delete.html')
    else:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)


@login_required #working
@permission_classes([IsAuthenticatedOrReadOnly])
def postvote(request, pk, uservote):
    """Vote on post"""
    post= get_object_or_404(Post, pk=pk,status=0)
    vote=''
    valueobj=''
    if request.method == "POST" and request.user != post.created_by: #users cannot like own posts
            try:
                vote= Vote.objects.get(user=request.user,post=post)
                valueobj= int(vote.value) # previous votes by the user
                uservote= int(uservote) # current user vote
                if valueobj != uservote: 
                    # if previous vote exists and is different from new vote then change the vote to neutralise previous vote
                        vote.delete()
                        upref= Vote()
                        upref.user= request.user
                        upref.post= post
                        upref.value= uservote
                        if uservote == 1 and valueobj != 1:
                                post.likes += 1
                                post.dislikes -=1
                        elif uservote == 2 and valueobj != 2:
                                post.dislikes += 1
                                post.likes -= 1
                        upref.save()
                        post.save()
                elif valueobj == uservote:
                        vote.delete()
                
                        if uservote == 1:
                                post.likes -= 1
                        elif uservote == 2:
                                post.dislikes -= 1
                        post.save()
                        
            except Vote.DoesNotExist: #no prior votes by user on post, either add an upvote or downvote
                upref= Vote()
                upref.user= request.user
                upref.post= post
                upref.value= uservote
                uservote= int(uservote)
                if uservote == 1:
                        post.likes += 1
                elif uservote == 2:
                        post.dislikes +=1
                upref.save()
                post.save()
    elif request.user ==  post.created_by:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)                          
    else:
        post= get_object_or_404(Post, pk=pk)
    return render (request, 'returntohome.html', {'post': post})


@login_required()
@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(['GET', 'POST', ])
def comment_create(request,pk):
    """create new comment"""
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    comment_form = CommentForm()
    context = {'post':post, 'comment_form':comment_form}
    if request.method == 'POST':
        Comment.objects.create(
        post = post,
        message = request.data["message"],
        created_at = datetime.now(),
        created_by = request.user)
    return HttpResponse(status=status.HTTP_202_ACCEPTED)

@login_required()
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_update(request, pk, id, status=0):
    """update comment, as long as post still active"""
    post = get_object_or_404(Post, pk=pk)
    comment = Comment.objects.get(post=post, id=id)
    update_comment = None
    comment_update_form = CommentUpdateForm()
    if request.method == 'POST' and comment.created_by == request.user:
        try:
            comment_update_form = CommentUpdateForm(request.POST,instance=comment)
            if comment_update_form.is_valid():
                update_comment = comment_update_form.save()
        except Comment.DoesNotExist:
            return render(request, 'comment_update.html', {'comments':comment, 'comment_update_form': comment_update_form})

    return render(request, 'comment_update.html', {'comments':comment, 'update_comment': update_comment,
                                           'comment_update_form': comment_update_form})


@login_required()
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_delete(request, pk, id):
    """delete own comments on posts"""
    post = get_object_or_404(Post, pk=pk)
    comment_to_delete = Comment.objects.get(post=post, id=id)
    if comment_to_delete.created_by == request.user:
        comment_to_delete.delete()
        return render(request, 'delete.html')
    else:
        return HttpResponse(status=status.HTTP_403_FORBIDDEN)
