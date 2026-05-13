from .models import User

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.dateformat import DateFormat

from rest_framework import serializers


import re
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "password"]

    def validate_username(self, value):
        value = value.strip().lower()

        if "@" in value:
            raise serializers.ValidationError(
                "Username cannot contain @ symbol."
            )

        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers and underscores."
            )

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Username already exists."
            )

        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(
            validated_data["password"]
        )

        return super().create(validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    joinedDate = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "first_name",
            "last_name",
            "username",
            "bio",
            "profile_pic",
            "location",
            "website",
            "joinedDate",
            "following",
            "followers",
            "posts",
        ]
        read_only_fields = ["id", "joinedDate", "following", "followers", "posts"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def get_joinedDate(self, obj):
        return DateFormat(obj.date_joined).format("F Y")

    def get_following(self, obj):
        return obj.follows.count()

    def get_followers(self, obj):
        return obj.followed_by.count()

    def get_posts(self, obj):
        return obj.user_posts.count()
