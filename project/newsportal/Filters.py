from django_filters import FilterSet, DateFilter, CharFilter, NumberFilter, ModelChoiceFilter
from django import forms
from .models import News, Author, Category, Article


class NewsFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Name'
    )
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Author'
    )

    creation_date__gte = DateFilter(
        field_name='creation_date',
        lookup_expr='date__gte',
        label='Created after',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    creation_date__lte = DateFilter(
        field_name='creation_date',
        lookup_expr='date__lte',
        label='Created before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    rating = NumberFilter(
        field_name="rating",
        lookup_expr="exact",
        label="Rating"
    )

    class Meta:
        model = News
        fields = ['title', 'creation_date__gte',
                  'creation_date__lte', 'author', 'rating']

class ArticleFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Name'
    )
    author = CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Author'
    )

    creation_date__gte = DateFilter(
        field_name='creation_date',
        lookup_expr='date__gte',
        label='Created after',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    creation_date__lte = DateFilter(
        field_name='creation_date',
        lookup_expr='date__lte',
        label='Created before',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    rating = NumberFilter(
        field_name="rating",
        lookup_expr="exact",
        label="Rating"
    )
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label="Category",
        empty_label="All Categories"
    )

    class Meta:
        model = Article
        fields = ['title', 'creation_date__gte',
                  'creation_date__lte', 'author', 'rating', 'category']


class AuthorFilter(FilterSet):
    username = CharFilter(
        field_name="user__username",
        lookup_expr="icontains",
        label="Name"
    )
    rating = NumberFilter(
        field_name="rating",
        lookup_expr="exact",
        label="Rating"
    )

    class Meta:
        model = Author
        fields = ['username', 'rating']