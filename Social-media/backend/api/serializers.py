from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.dateformat import DateFormat

from rest_framework import serializers
from api.models import *

user = get_user_model()



class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    avatar = serializers.ImageField(source="profile_pic")

    class Meta:
        model = User
        fields = ["name", "username", "avatar"]

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(source="user", read_only=True)
    content = serializers.CharField(source="message")
    created_at = serializers.DateTimeField(source="date", format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    likesCount = serializers.SerializerMethodField()
    repostsCount = serializers.SerializerMethodField()
    repliesCount = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    isReposted = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    media = serializers.FileField(write_only=True, required=False)
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "likesCount",
            "repostsCount",
            "repliesCount",
            "isLiked",
            "isReposted",
            "image",
            "media",
        ]
        read_only_fields = ["created_at"]
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
    def get_likesCount(self, obj):
        return obj.like.count()
        
    def get_repostsCount(self, obj):
        return 0
    
    def get_repliesCount(self, obj):
        return obj.post_comments.count()
        
    def get_isLiked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like.filter(id=request.user.id).exists()
        return False
    def get_isReposted(self, obj):
        return False
        
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.media:
            return request.build_absolute_uri(obj.media.url)
        return None
        
class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = user
        fields = [
            'id', 'email', 'username', 'password'
        ]
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(RegisterUserSerializer, self).create(validated_data)
        # password = validated_data.pop('password')
        # user = User.objects.create(**validated_date)
        # return user

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

