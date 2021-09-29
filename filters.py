import django_filters
from .models import Post
from django_filters import CharFilter, NumberFilter


class PostFilter(django_filters.FilterSet):
    """ filter / search bar accross top of screen """
    class Meta:
        model = Post
        fields = ['topic','title','content', 'status']

    def filter_search(self, qs, name, value):
        if value:
            return qs.filter((
                Q(title__icontains=value) |
                Q(content__icontains=value)
            ))
        return qs