from .auth import User

#django
from django.db.models import Q, Count

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