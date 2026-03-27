from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics, filters, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import LastViewedPost
from .models import Comment
from .models import Like
from .models import Post
from .models import Favorite
from .serializers import PostSerializer
from .serializers import FavoriteSerializer
from .serializers import CommentSerializer
from .serializers import LikeSerializer
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsCommentOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated


# ================== Post list / create ==================
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'content']
    filterset_fields = ['author__username']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# ================== Post detail / update / delete ==================
class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.all()



class FavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        from django.shortcuts import get_object_or_404
        post = get_object_or_404(Post, id=post_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)
        if not created:
            favorite.delete()
            return Response({'message': 'Removed from favorites'}, status=200)
        return Response({'message': 'Added to favorites'}, status=201)


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)




class LastViewedPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(
            lastviewedpost__user=self.request.user
        )[:10]


def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()

    instance.view_count += 1
    instance.save()


    if request.user.is_authenticated:
        from .models import LastViewedPost
        LastViewedPost.objects.update_or_create(
            user=request.user,
            post=instance
        )

    serializer = self.get_serializer(instance)
    return Response(serializer.data)



class LikeDislikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Agar post like/dislike qilinmagan bo'lsa, default like=True
        Agar allaqachon bor bo'lsa, toggle qilinadi
        """
        post = get_object_or_404(Post, id=post_id)
        like_obj, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            # Toggle like/dislike
            like_obj.is_like = not like_obj.is_like
            like_obj.save()
            action = "Like" if like_obj.is_like else "Dislike"
            return Response({"message": f"Post {action} qilindi"}, status=status.HTTP_200_OK)
        return Response({"message": "Post Like qilindi"}, status=status.HTTP_201_CREATED)


class LikeListView(generics.ListAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Like.objects.filter(user=self.request.user)

