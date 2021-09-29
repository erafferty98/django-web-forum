from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','topic','content',
                    'created_at','created_by',
                    'updated_by', 'updated_at',
                    'status', 'likes', 'dislikes')


#class CommentSerializer(serializers.ModelSerializer):
#    post=PostSerializer(read_only=True)
#    class Meta:
#        model = Comment
#        fields = ('post','message','created_at',
#                    'created_by')
        