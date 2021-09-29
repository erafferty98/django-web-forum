path('sport', SportView.as_view(), name ='sport'),
path('sport/<int:pk>/', SportDetailView.as_view(), name='sport_detail'),
path('health', HealthView.as_view(), name ='health'),
path('health/<int:pk>/', HealthDetailView.as_view(), name='health_detail'),
path('tech', TechView.as_view(), name ='tech'),
path('tech/<int:pk>/', TechDetailView.as_view(), name='tech_detail'),
path('politics', PoliticsView.as_view(), name ='politics'),
path('politics/<int:pk>/', PoliticsDetailView.as_view(), name='politics_detail'),


class SportList(ListView):
    queryset = Topic.objects.filter(subject="Sport").order_by('-created_on')
    template_name = 'sport.html'

class HealthList(ListView):
    queryset = Topic.objects.filter(subject="Health").order_by('-created_on')
    template_name = 'health.html'

class TechList(ListView):
    queryset = Topic.objects.filter(subject="Technology").order_by('-created_on')
    template_name = 'tech.html'

class PoliticsList(ListView):
    queryset = Topic.objects.filter(subject="Politics").order_by('-created_on')
    template_name = 'politics.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'



  <form method="POST">
    <h4> Delete Post</h4>
    {% csrf_token %}
    <input type="submit" value="Confirm Delete" class="btn btn-danger btn-large">
    <a href="{% url 'posts:post' username=user.username pk=object.pk %}" class="btn btn-simple btn-large btn-default">Cancel</a>
  </form>


  def post_archive(request,year,month):
    post_list = Post.objects.filter(created_at__year=year, 
                                    created_at__month=month,
                                    ).order_by("-created_at")
    return render(request,'index.html',{'post_list':post_list})

path('archives/(<int:year>[0-9]{4})/(<int:month>[0-9]{1,2})/',views.post_archive, name='archives'),

    {% for date in date_list %}
        <li>
            <a href="{% url 'post:archives' date.year date.month %}">
                {date. Year} year {date. Month} month
            </a>
        </li>
    {% endfor %}


                <a href="{% url 'post_detail' post.slug  %}" class="btn btn-primary">Read More &rarr;</a>
                {% if user.is_authenticated %}
                  <a href="{% url 'post_update' post.slug  %}" class="btn btn-primary">Update Post &rarr;</a>
                {% endif %}


        <div id="likesview">
        <button type="button" class="collapsible">Toggle Posts filtered by likes</button>
          <div class="content">
            {% for post in post %} %}
            <p>
              <h2>{{ post.title }}</h2>
              <h4>{{post.content|slice:":50" }}</h4>
              <h6>Author: {{ post.created_by }}</h6>
              <h6>Created on: {{ post.created_at}}</h6>
              <h6>Last updated: {{ post.updated_at}}</h6>
              <h6>Topic: {{post.topic }}</h6>
              <h6>Likes: {{ post.likes }} | Dislikes: {{ post.dislikes }}</h6>
            </p>
            {% endfor %}
          </div>
          {% endif %}




    'DEFAULT_PAGINATION_CLASS': (
        'rest_framework.pagination.CursorPagination',
    ),
    'PAGE_SIZE': (
        10
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.TemplateHTMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer'
    ),

mary
{
    "access_token": "cVi7bFruCnGR3rzKrZytMHY8IiTSpC",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "TAK68ngu3xavBADvZiPZIIni7oLZbV"
}

olga
{"username": "olga", "password": "olgaolga123"}
{
    "access_token": "kTAgvfm57a74uNM3PeIebysZ5TcC2D",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "is0fznSYltwu8uXm48D0iavssOQ3HB"
}

nick
{
    "access_token": "Y2YU9XTPb1h2JaatJf5eW1P6VM01pJ",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "JU0JnLDPvKpVaWgyEjIuPnOMlkFL2Z"
}
nestor
{
    "access_token": "wbWxr8ENlLzGtvibU40hHn6N5oFHG5",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "fz6wkS2RtXT4QUV500lT7dbEyS2NKD"
}
admin{"username": "admin", "password": "adminadmin123"}
{
    "access_token": "afiqn36O8hl0kt7tYQehG19bEe2T1A",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write",
    "refresh_token": "Gwh9oej2hcDsNuTgF5zvciUlZCatyi"
}



class CommentViewSet(viewsets.ViewSet):

    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request):
        #if request.accepted_renderer.format == 'html':
        queryset=Comment.objects.all().order_by('-created_at')
        serializer = CommentSerializer(queryset,many=True)
        context = {'Comments': serializer.data}
        return Response(context)
        #return super(CommentViewSet, self).Comment_list(self, request)

    def create(self, request):
        #if request.accepted_renderer.format == 'html':
        Comment.objects.create(
            id=id,
            post = request.data["post"],
            message = request.data["reply"],
            created_at = datetime.now(),
            created_by = request.user)
        return Response(status=status.HTTP_202_ACCEPTED,template_name = 'posts/post_detail.html')
        #return super(CommentViewSet, self).create(self, request)

    def detail(self, request, pk=None):
        #if request.accepted_renderer.format == 'html':
        queryset = Comment.objects.filter(status=0).order_by("-created_at")
        Comment = get_object_or_404(queryset)
        serializer = CommentSerializer(Comment)
        return Response(serializer.data,template_name = 'posts/post_detail.html')
        #return super(CommentViewSet, self).detail(self, request,pk=None)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        #if request.accepted_renderer.format == 'html':
        serialized = CommentSerializer(request.user, data=request.data, partial=True)
        return Response(status=status.HTTP_202_ACCEPTED,template_name = 'comment_update.html')
        #return super(CommentViewSet, self).partial_update(self, request,pk=None)

    def destroy(self, request, pk=None):
        #if request.accepted_renderer.format == 'html':
        instance = Comment.objects.get()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT,template_name = 'posts/delete.html')
        #return super(CommentViewSet, self).destroy(self, request,pk=None)

def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

#    path('', views.post_list, name='home'),
#    path('<slug:slug>/', views.post_detail, name='post_detail'),
#    path('<slug:slug>/update/', views.post_update, name='post_update'),
#    path('<slug:slug>/delete/',views.post_delete, name='post_delete'),
#    path('<slug:slug>/<int:id>/comment-update/', views.comment_update, name='comment_update'),
#    path('<int:id>/comment-delete/', views.comment_delete, name='comment_delete'),
#    path('<slug:slug>/preference/<int:uservote>/', views.postvote, name='uservote'),
#    path('archives/(<int:year>[0-9]{4})/(<int:month>[0-9]{1,2})/',views.post_archive, name='archives'),



#@permission_classes([IsAuthenticatedOrReadOnly])
#def post_list(request):
#    myFilter = PostFilter(request.GET, queryset=Post.objects.filter(status=0).order_by("-created_at"))
#    post = myFilter.qs
#    likeFilter = PostFilter(request.GET, queryset=Post.objects.filter(status=0).order_by("-likes","dislikes"))
#    new_post = None
#    if request.method == 'POST':
#        post_form = PostForm(request.POST)
#        if post_form.is_valid():
#            new_post = post_form.save(commit=False)
#            new_post.created_at = datetime.now
#            new_post.slug = slugify(new_post.title)
#            new_post.status = 0
#            new_post.updated_by = request.user
#            new_post.save()
#    else:
#        post_form = PostForm()
#    return render(request, 'index.html', {'posts': post, 'new_post': new_post, 'post_form': post_form,'myFilter': myFilter, 'likeFilter':likeFilter})
#
#@permission_classes([IsAuthenticatedOrReadOnly])
#def post_detail(request, slug):
#    post = get_object_or_404(Post, slug=slug, status=0)
#    comments = post.comments
#    new_comment = None
#    if request.method == 'POST':
#        comment_form = CommentForm(data=request.POST)
#        if comment_form.is_valid():
#            new_comment = comment_form.save(commit=False)
#            new_comment.post = post
#            new_comment.save()
#    else:
#        comment_form = CommentForm()
#
#    return render(request, 'post_detail.html', {'posts': post,
#                                           'comments': comments,
#                                           'new_comment': new_comment,
#                                           'comment_form': comment_form})
#
#@login_required()
#@permission_classes([IsAuthenticated])
#def post_update(request, slug, status=0):
#    post = Post.objects.get(slug=slug)
#    update_post = None
#    if request.method == 'POST' and request.user == post.created_by:
#        post_update_form = PostUpdateForm(request.POST, instance=post)
#        if post_update_form.is_valid():
#            update_post = post_update_form.save(commit=False)
#            update_post.updated_at = datetime.now()
#            update_post.updated_by = request.user
#            update_post.save()
#    else:
#        post_update_form = PostUpdateForm()
#    return render(request, 'posts/post_update.html', {'posts': post, 'update_post': update_post, 'post_update_form': post_update_form})
#
#
#@login_required()
#@permission_classes([IsAuthenticated])
#def post_delete(request,slug):
#    post_to_delete = Post.objects.get(slug=slug)
#    post_to_delete.delete()
#    return render(request, 'delete.html')
#
#
#def post_archive(request,year,month):
#    post_list = Post.objects.filter(created_at__year=year, 
#                                    created_at__month=month,
#                                    ).order_by("-created_at")
#    return render(request,'index.html',{'post_list':post_list})
#
#
#@login_required()
#@permission_classes([IsAuthenticated])
#def comment_update(request, slug, id, status=0):
#    comment = Comment.objects.get(id=id)
#    update_comment = None
#    if request.method == 'POST' and comment.created_by == request.user:
#        try:
#            comment_update_form = CommentUpdateForm(request.POST,instance=comment)
#            if comment_update_form.is_valid():
#                update_comment = comment_update_form.save()
#            else:
#                comment_update_form = CommentUpdateForm()
#        except Comment.DoesNotExist:
#            return render(request, 'posts/comment_update.html', {'comments':comment, 'comment_update_form': comment_update_form})
#
#    return render(request, 'posts/comment_update.html', {'comments':comment, 'update_comment': update_comment,
#                                           'comment_update_form': comment_update_form})
#
#
#@login_required()
#@permission_classes([IsAuthenticated])
#def comment_delete(request, id, status=0):
#    comment_to_delete = Comment.objects.get(id=id)
#    comment_to_delete.delete()
#    return render(request, 'delete.html')
#

        <ul class="navbar-nav ml-auto">
          <a href="{% url 'post_update' posts.slug  %}" class="btn btn-primary">Update Post! &rarr;</a>
        </ul>


<div class="container">
    <div class="col-md-8 card mb-4  mt-3 ">
      <div class="card-body">
        <h2>{{ comments.count }} comment(s)</h2>
        {% for comment in comments.all %}
        <div class="comments" style="padding: 10px;">
          <p class="font-weight-bold">
            <h5>Comment by {{ comment.created_by }} on {{ comment.post }}</h5>
            <span class=" text-muted font-weight-normal">
              {{ comment.created_at }}
            </span>
          </p>
          <h3>{{ comment.message | linebreaks }}</h3>
          {% if user.is_authenticated %}
          <ul class="navbar-nav ml-auto">
            <a href="{% url 'comment_update' posts.slug comment.id  %}" class="btn btn-primary">Update Comment! &rarr;</a>
          </ul>
        {% endif %}
        </div>
        {% endfor %}
      </div>
    </div>
    {% if user.is_authenticated %}
    <div class="col-md-8 card mb-4  mt-3 ">
      <div class="card-body">
        <h3>Leave a comment</h3>
        <form method="post" style="margin-top: 1.3em;">
          {{ comment_form | crispy }}
          {% csrf_token %}
          <button type="submit" class="btn btn-primary  btn-lg">Submit</button>
        </form>
      </div>
    </div>
    {% endif %}
  </div>
</div>