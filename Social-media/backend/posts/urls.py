from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# app_name = "post"

router = DefaultRouter()
router.register(r"", views.PostViewSet, basename="post")

urlpatterns = [path("", include(router.urls))]
