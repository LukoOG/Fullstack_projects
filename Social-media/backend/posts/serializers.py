from .models import Post

from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.dateformat import DateFormat

from rest_framework import serializers
User = get_user_model()

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
    likes_count = serializers.SerializerMethodField()
    reposts_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_reposted = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    media = serializers.FileField(write_only=True, required=False)
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "created_at",
            "likes_count",
            "reposts_count",
            "replies_count",
            "is_liked",
            "is_reposted",
            "image",
            "media",
        ]
        read_only_fields = ["created_at"]
    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["user"] = request.user
        return super().create(validated_data)
    def get_likes_count(self, obj):
        return obj.like.count()
        
    def get_reposts_count(self, obj):
        return 0
    
    def get_replies_count(self, obj):
        return obj.post_comments.count()
        
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.like.filter(id=request.user.id).exists()
        return False
    def get_is_reposted(self, obj):
        return False
        
    def get_image(self, obj):
        request = self.context.get('request')
        if obj.media:
            return request.build_absolute_uri(obj.media.url)
        return None
        


