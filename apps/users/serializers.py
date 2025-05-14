from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users.models import Profile, UserAccount


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "id",
            "username",
            "email",
        )
        read_only_fields = ("id",)


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "id",
            "username",
            "email",
            "password",
        )
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = UserAccount.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if user and user.is_active:
            return user
        return serializers.ValidationError({"error": "Invalid credentials"})


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("bio",)


class ProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("avatar",)
