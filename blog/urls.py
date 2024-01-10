from django.urls import path
from .views import BlogPostListView

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blog_post_list'),
    path('<str:category_name>/', BlogPostListView.as_view(), name='blog_post_list_by_category'),
]