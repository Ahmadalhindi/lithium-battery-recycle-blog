from django.urls import path
from .views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path(
        '<str:category_name>/',
        PostListView.as_view(),
        name='post_list_by_category'
    ),
]
