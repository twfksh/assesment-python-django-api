from django.urls import path

from apps.users.views import (
    UserRegisterAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    TokenRefreshAPIView,
    UserAPIView,
    UserProfileAPIView,
    UserProfileAvatarAPIView,
)

app_name = "users"

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),
    path("refresh-token/", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("", UserAPIView.as_view(), name="user-info"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    path("profile/avatar/", UserProfileAvatarAPIView.as_view(), name="profile_avatar"),
]
