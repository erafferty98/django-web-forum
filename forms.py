from django import forms
from .models import Comment, Post, CATEGORY


class PostForm(forms.ModelForm):
    #required fields for form, others populated automatically in views
    topic = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=(CATEGORY)
    )
    class Meta:
        model = Post
        fields = ('title', 'topic', 'content', 'expiry_time')

class PostUpdateForm(forms.ModelForm):
    #required fields for update form, others populated automatically in views
    class Meta:
        model = Post
        fields = ('content','status')

class CommentForm(forms.ModelForm):
    #required fields for comment, others populated automatically in views
    class Meta:
        model = Comment
        fields = ('message', 'created_by')

class CommentUpdateForm(forms.ModelForm):
    #required fields for comment update, others populated automatically in views
    class Meta:
        model = Comment
        fields = ('message',)