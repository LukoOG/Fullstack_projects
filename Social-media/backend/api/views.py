#
from .auth import User

#django
from django.db.models import Q

#rest_framework
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import UserProfileSerializer, PostSerializer
from .models import *
#rest_framework simple jwts


#View Functions
@api_view(["GET"])
def index(request):
    context = {
        'list of url routes': '/index',
    }
    return Response(context)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Custom permission to only allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "username"
    permission_classes = [IsOwnerOrReadOnly]
    
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_follow(self, request, username=None):
        user = request.user
        user_profile = self.get_object()#target user account
        if user.follows.filter(id=user_profile.id).exists():
            user.follows.remove(user_profile)
            following = False
        else:
            user.follows.add(user_profile)
            following = True
        user.save()
        user_profile_follows = user_profile.followed_by.count() #how many accounts follow target user after update
        
        serializer = self.get_serializer(user_profile, context={"request":request})
        return Response({ "following":following, "follows":user_profile_follows }, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            context={"request":request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.perform_create(serializer)
        return Response( serializer.data,status=status.HTTP_201_CREATED)
        
    @action(detail=True, methods=["get"])
    def following(self, request, username=None):
        """Return all users this user is following"""
        user = self.get_object()
        following = user.followed_by.all()  # assuming you have follows ManyToMany
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['get'])
    def followers(self, request, username=None):
        user = self.get_object()
        followers = user.follows.all()
        serializer = self.get_serializer(followers, many=True)
        return Response(serializer.data)
    @action(detail=False, methods=['get'])
    def me(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response({"error": "no logged in user"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(request.user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    
        
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("user").prefetch_related("like").all().order_by("-date")
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get("username")
        if username:
            queryset = queryset.filter(user__username=username)
        return queryset
    
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        
        if post.like.filter(id=user.id).exists():
            post.like.remove(user)
            liked = False
        elif not post.like.filter(id=user.id).exists():
            post.like.add(user)
            liked = True
        post.save()
        
        #serializer = self.get_serializer(post, context={"request": request})
        
        return Response({
            "liked":liked,
            "likes":post.like.count(),
        }, status=status.HTTP_200_OK)
        
@action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
def feed(self, request):
    user = request.user
    following = user.follows.all()

    posts = Post.objects.filter(
        Q(user__in=following) | Q(user=user)
    ).select_related("user").prefetch_related("likes")

    if not posts.exists():
        posts = Post.objects.all()

    posts = posts.annotate(
        likes_count=Count("likes")
    ).order_by("-likes_count", "-date")

    serializer = self.get_serializer(posts, many=True)
    return Response(serializer.data)