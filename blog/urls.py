from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentRetrieveUpdateDestroyView, \
    CommentListCreateView, FavoriteListView, FavoriteToggleView, LastViewedPostListView, LikeListView, \
    LikeDislikeToggleView

urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
    path('posts/<int:post_id>/favorite/', FavoriteToggleView.as_view(), name='favorite-toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
    path('posts/last-viewed/', LastViewedPostListView.as_view(), name='last-viewed-list'),
    path('posts/<int:post_id>/like/', LikeDislikeToggleView.as_view(), name='like-toggle'),
    path('likes/', LikeListView.as_view(), name='like-list'),
]