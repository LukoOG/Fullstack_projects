from . import auth, views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", views.UserProfileViewSet, basename="user")

urlpatterns = [
    path("csrf", auth.get_csrf),
    path("register", auth.RegisterView.as_view(), name="register"),
    path("login", auth.LoginTokenObtainPairView.as_view(), name="login"),
    path("logout", auth.LogoutView.as_view(), name="logout"),
    path(
        "token/refresh",
        auth.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

urlpatterns.append(path("", include(router.urls)))
