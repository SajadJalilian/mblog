from django.shortcuts import render, get_objec_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.view.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Category, Comment


class PostListView(ListView):
    model = Post
    template_name = 'Blog/home.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']
    paginate_by = 5


class UserPostListView(ListView):
    midel = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_objec_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-pub_date')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().from_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.required.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CategoryListView(ListView):
    model = Category
    template_object_name = 'blog/category.html'
    context_object_name = 'categories'
    ordering = ['title']
    paginate_by = 5


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['title']


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['title']


class CategoryDeteleView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = '/'


class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    ordering = ['-pub_date']


class CommentCreateView(CreateView):
    model = Comment
    fields = ['name', 'content']


class CommentDeleteView(DeleteView):
    model = Comment


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})