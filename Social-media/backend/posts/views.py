#
from ..accounts.auth import User

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
        ).select_related("user").prefetch_related("like")

        if not posts.exists():
            posts = Post.objects.all()

        posts = posts.annotate(
            likes_count=Count("like")
        ).order_by("-likes_count", "-date")
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # fallback (if pagination disabled)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)