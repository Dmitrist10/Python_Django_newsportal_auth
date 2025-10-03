from typing import Any
# from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, DeleteView, CreateView
from .models import Article, News, Author
from .Filters import NewsFilter, ArticleFilter, AuthorFilter
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin


class HomePage(TemplateView):
    template_name = "newsportal/home.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["best_Author"] = Author.objects.order_by("-rating").first()
        context["best_News"] = News.objects.order_by("-rating").first()
        # context["newest_Article"] = Article.objects.order_by(
        #     "-creation_date").first()
        context["best_Article"] = Article.objects.order_by(
            "-rating").first()
        
        context['is_not_premium'] = not self.request.user.groups.filter(
            name='premium').exists()
        
        return context

@login_required
def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='premium')
    if not request.user.groups.filter(name='premium').exists():
        premium_group.user_set.add(user)

    return redirect('/')

@login_required
def startAuthor(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)

    return redirect('/')

class MyPage(LoginRequiredMixin, TemplateView):
    template_name = "newsportal/mypage.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['is_premium'] = self.request.user.groups.filter(name='premium').exists()
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()

        return context


class Article_Detail(DetailView):
    model = Article
    template_name = "newsportal/Article/Article_Details.html"
    context_object_name = 'article'


class Article_List(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = "newsportal/Article/Article_List.html"
    ordering = ["-creation_date"]
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = ArticleFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filter
        return context


class New_Detail(DetailView):
    model = News
    template_name = "newsportal/News/News_Details.html"
    context_object_name = 'new'


class New_List(ListView):
    model = News
    template_name = "newsportal/News/News_List.html"
    context_object_name = 'news'
    ordering = ["-creation_date"]
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = NewsFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filter
        return context


class Author_Detail(DetailView):
    model = Author
    template_name = "newsportal/Author/Author_Details.html"
    context_object_name = 'author'


class Author_List(ListView):
    model = Author
    template_name = "newsportal/Author/Author_List.html"
    context_object_name = 'authors'
    ordering = ["-rating"]
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter = AuthorFilter(self.request.GET, queryset)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filter
        return context


# def create_New(request):
#     form = NewsForm()

#     if request.method == "POST":
#         form = NewsForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return HttpResponseRedirect("/main/news")

#     return render(request, "newsportal/News/News_edit.html", {'form': form})

# def create_Article(request):
#     form = ArticleForm()

#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         if form.is_valid:
#             form.save()
#             return HttpResponseRedirect("/main/articles")

#     return render(request, "newsportal/Article/Article_edit.html", {'form': form})

class News_Form_Create(PermissionRequiredMixin , LoginRequiredMixin, CreateView):
    permission_required = ('newsportal.add_news')

    form_class = NewsForm
    model = News

    template_name = "newsportal/News/News_edit.html"

    def form_valid(self, form):
        author = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


class News_Form_Edit(PermissionRequiredMixin , LoginRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_news')


    form_class = NewsForm
    model = News


    template_name = "newsportal/News/News_edit.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=self.request.user)


class News_Form_Delete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_news')

    model = News
    context_object_name = 'new'

    template_name = "newsportal/News/News_Delete.html"
    success_url = reverse_lazy('New_List')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=self.request.user)



class Articles_Form_Create(PermissionRequiredMixin , LoginRequiredMixin, CreateView):
    permission_required = ('newsportal.add_article')

    form_class = ArticleForm
    model = Article

    template_name = "newsportal/Article/Article_edit.html"

    def form_valid(self, form):
        author, created = Author.objects.get_or_create(user=self.request.user)
        form.instance.author = author
        return super().form_valid(form)


class Articles_Form_Edit(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('newsportal.change_article')

    form_class = ArticleForm
    model = Article

    template_name = "newsportal/Article/Article_edit.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=self.request.user)



class Articles_Form_Delete(PermissionRequiredMixin , LoginRequiredMixin, DeleteView):
    permission_required = ('newsportal.delete_article')

    model = Article
    context_object_name = 'article'

    template_name = "newsportal/Article/Article_Delete.html"
    success_url = reverse_lazy('Article_List')

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(author__user=self.request.user)
