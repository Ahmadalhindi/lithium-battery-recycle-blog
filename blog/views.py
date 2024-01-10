from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Category, Post

class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by("created_at")
    template_name = 'post_list.html'
    paginate_by = 4

    def get_queryset(self):
        category_name = self.kwargs.get('category_name', None)
        if category_name:
            return Post.objects.filter(categories__name=category_name)
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context
