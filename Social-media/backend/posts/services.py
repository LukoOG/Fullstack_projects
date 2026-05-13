from django.db.models import Q, Count

from accounts.models import User
from .models import Post


def get_posts_by_username(username=None):
    """
    Return posts optionally filtered by username.
    """
    queryset = (
        Post.objects.select_related("user")
        .prefetch_related("likes")
        .all()
        .order_by("-date")
    )
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset


def toggle_post_like(post, user):
    """
    Toggles the like of a post for a user.
    Returns a dict with liked status and total likes.
    """
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.like.add(user)
        liked = True

    post.save()
    return {
        "liked": liked,
        "likes": post.likes.count(),
    }


def get_user_feed(user: User):
    """
    Returns posts for a user's feed:
    - Authenticated users: posts from people they follow + their own posts
    - Unauthenticated users: all posts
    Annotated with likes_count, ordered by likes_count desc then date desc.
    """
    if user and user.is_authenticated:
        following = user.follows.all()
        posts = Post.objects.filter(Q(user__in=following) | Q(user=user))
    else:
        posts = Post.objects.all()

    posts = posts.select_related("user").prefetch_related("likes")
    posts = posts.annotate(likes_count=Count("likes")).order_by("-likes_count", "-date")
    return posts
