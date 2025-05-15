from django.shortcuts import get_list_or_404
from rest_framework import permissions, status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.models import Tag, Post, Comment
from apps.posts.serializers import (
    TagReadSerializer,
    PostReadSerializer,
    PostWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
)

from apps.posts.permissions import IsAuthorOrReadOnly


class TagViewSet(ReadOnlyModelViewSet):
    """
    List and Retriever post tags
    """

    queryset = Tag.objects.all()
    serializer_class = TagReadSerializer
    permission_classes = (permissions.AllowAny,)


class PostViewSet(ModelViewSet):
    """
    CRUD operation endpoints for posts
    """

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer
        return PostReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class CommentViewSet(ModelViewSet):
    """
    CRUD operation endpoints for post comments
    """

    queryset = Comment.objects.all()

    def get_queryset(self):
        result = super().get_queryset()
        post_id = self.kwargs.get("post_id")
        return result.filter(post_id=post_id)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return CommentWriteSerializer
        return CommentReadSerializer

    def get_permissions(self):
        if self.action in ("create"):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class LikePostAPIView(APIView):
    """Like or Dislike a post"""

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        post = get_list_or_404(Post, pk=pk)

        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)
