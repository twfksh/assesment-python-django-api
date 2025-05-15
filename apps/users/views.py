from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    ProfileAvatarSerializer,
)
from apps.users.models import Profile


User = get_user_model()


class UserRegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        response = Response(data, status=status.HTTP_201_CREATED)
        # set http-only cookie
        response.set_cookie(
            key="access_token",
            value=str(token.access_token),
            httponly=True,
            samesite="None",
            secure=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(token),
            httponly=True,
            samesite="None",
            secure=True,
        )
        return response


class UserLoginAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        response = Response(data, status=status.HTTP_200_OK)
        # set http-only cookie
        response.set_cookie(
            key="access_token",
            value=str(token.access_token),
            httponly=True,
            samesite="None",
            secure=True,
        )
        response.set_cookie(
            key="refresh_token",
            value=str(token),
            httponly=True,
            samesite="None",
            secure=True,
        )
        return response


class UserLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"detail": "Logout failed", "error": f"{str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TokenRefreshAPIView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh") or request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({"refresh": ["This field is required."]}, status=400)
        # Set the refresh token in request.data for the parent class
        if hasattr(request.data, "mutable") and not request.data.mutable:
            request.data.mutable = True
            request.data["refresh"] = refresh_token
            request.data.mutable = False
        else:
            request.data["refresh"] = refresh_token
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access_token = response.data["access"]
            refresh_token = response.data["refresh"]
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                samesite="None",
                secure=True,
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="None",
                secure=True,
            )
        return response


class UserAPIView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile


class UserProfileAvatarAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileAvatarSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile
