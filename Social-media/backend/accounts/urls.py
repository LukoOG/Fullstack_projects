from . import auth, views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# app_name = "accounts"

router = DefaultRouter()
router.register(r"users", views.UserProfileViewSet, basename="user")

urlpatterns = [
    path("auth/csrf", auth.get_csrf),
    path("auth/register", auth.RegisterView.as_view(), name="register"),
    path("auth/login", auth.LoginTokenObtainPairView.as_view(), name="login"),
    path("auth/logout", auth.LogoutView.as_view(), name="logout"),
    path(
        "auth/token/refresh",
        auth.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

urlpatterns.append(path("", include(router.urls)))
