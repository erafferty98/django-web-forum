import math
from django.db import models
from django.utils.text import Truncator
from django.contrib.auth.models import User
from users.serializers import CreateUserSerializer
from django.utils.html import mark_safe
from markdown import markdown
from datetime import datetime, timedelta
import pytz
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

#make datetimes same type
utc = pytz.UTC

#categories of topic
CATEGORY = [
    ("Health", "Health"),
    ("Politics","Politics"),
    ("Sport","Sport"),
    ("Tech","Tech"),
]

#status of post
STATUS = (
    (0,"Live"),
    (1,"Expired"),
    )
    

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    topic = models.TextField(choices=CATEGORY, default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    created_by = models.ForeignKey(User, related_name="post_created_by", on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='post_updated_by', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS, default=0)
    expiry_time = models.DateTimeField()
    likes= models.IntegerField(default=0)
    dislikes= models.IntegerField(default=0)

    class Meta:
        #ordering by creation and update date so active threads are not archived
        ordering = ['-created_at','-updated_at'] 

    def __str__(self):
        return self.title
    
    def expire_post(self):
        """ expire posts that are old, have an expired status, or are highly disliked"""
        if (self.created_at or self.updated_at) < \
            utc.localize((datetime.today() - timedelta(hours=1))):
            self.status = 1
        elif self.dislikes >= 4:
            self.status = 1
        elif self.expiry_time <= datetime.today():
            self.status = 1
        return self.status

    def generate_slug(self):
        generated_slug = slugify(self.title)
        return generated_slug
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments_post', on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    def generate_slug(self):
        generated_slug = slugify(self.message)
        return generated_slug

    class Meta:
        ordering = ['created_at']

class Vote(models.Model):
    user= models.ForeignKey(User, related_name = 'vote',on_delete=models.CASCADE)
    post= models.ForeignKey(Post, related_name = 'vote',on_delete=models.CASCADE)
    value= models.IntegerField()

    def __str__(self):
        return str(self.value)

    class Meta:
       unique_together = ("user", "post", "value")