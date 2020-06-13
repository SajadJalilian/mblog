from django.shortcuts import render, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Article, Category, Comment


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    ordering = ['-pub_date']
    paginate_by = 5


class UserArticleListView(ListView):
    model = Article
    template_name = 'blog/user_articles.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-pub_date')


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content']

    def form_invalid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == Article.author:
            return True
        return False


class ArticleDeleteView(DeleteView):
    model = Article
    success_url ='/'

    def test_func(self):
        article = self.get_object()
        if self.request.user == article.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})