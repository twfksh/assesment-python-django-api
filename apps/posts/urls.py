from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.posts.views import (
    TagViewSet,
    PostViewSet,
    CommentViewSet,
    LikePostAPIView,
)

app_name = "posts"

router = DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)
router.register(r"", PostViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("like/<int:pk>/", LikePostAPIView.as_view(), name="like-post"),
]
