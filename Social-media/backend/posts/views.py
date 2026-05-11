#
from accounts.models import User

# django
from django.db.models import Q, Count

# rest_framework
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import PostSerializer
from .models import *
from . import services


class PostViewSet(viewsets.ModelViewSet):
    queryset = (
        Post.objects.select_related("user")
        .prefetch_related("like")
        .all()
        .order_by("-date")
    )
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.request.query_params.get("username")
        return services.get_posts_by_username(username)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def toggle_like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        result = services.toggle_post_like(post, user)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[])
    def feed(self, request):
        user = request.user
        posts = services.get_user_feed(user)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # fallback (if pagination disabled)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)
