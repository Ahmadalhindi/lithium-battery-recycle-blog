from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path(
        'delete_comment/<slug:slug>',
        views.PostDetail.as_view(),
        name='delete_comment'
    ),
]
