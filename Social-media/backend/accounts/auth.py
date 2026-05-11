from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from .serializers import RegisterUserSerializer

# rest_framework
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Serializer errors:", serializer.errors)
            return Response({"errors": serializer.errors}, status=400)
        user = serializer.save()

        token_serializer = EmailTokenObtainPairSerializer(
            data={"email": user.email, "password": request.data.get("password")}
        )
        token_serializer.is_valid(raise_exception=True)
        data = token_serializer.validated_data
        access_token = data["access"]
        refresh_token = data["refresh"]

        response = Response(
            {
                "success": True,
                "user": {"id": user.id, "email": user.email, "username": user.username},
            },
            status=status.HTTP_201_CREATED,
        )
        response.set_cookie(
            key="accessToken",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 15,
        )

        response.set_cookie(
            key="refreshToken",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="None",
            max_age=60 * 60 * 24 * 7,
        )

        return response


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        token["avatar"] = user.profile_pic.url
        return token


class LoginTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        print(response)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            access = data.get("access")
            refresh = data.get("refresh")

            # Set cookies
            response.set_cookie(
                key="accessToken",
                value=access,
                httponly=True,
                secure=True,
                samesite="None",
                max_age=60 * 15,
            )

            response.set_cookie(
                key="refreshToken",
                value=refresh,
                httponly=True,
                secure=True,
                samesite="None",
                max_age=60 * 60 * 24 * 7,
            )

            response.data.pop("access", None)
            response.data.pop("refresh", None)
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh")
        if not refresh:
            return Response(
                {"detail": "Refresh token missing"}, status=status.HTTP_401_UNAUTHORIZED
            )
        try:
            old_refresh = RefreshToken(refresh)

            user_id = old_refresh["user_id"]
            user = User.objects.get(id=user_id)
            print(user)

            old_refresh.blacklist()

            new_refresh = RefreshToken.for_user(user)      
            new_refresh["email"] = user.email
            new_refresh["username"] = user.username
            new_refresh["avatar"] = user.profile_pic.url
            
            access = str(new_refresh.access_token)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        """
        response.set_cookie(
            key="accessToken",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 15,
        )
        """
        return Response(
            {"success": True, "refresh": str(new_refresh), "access": access}
        )


class LogoutView(APIView):
    def post(self, request):
        response = Response({"success": True})
        response.delete_cookie("accessToken")
        response.delete_cookie("refreshToken")
        return response


@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({"detail": "CSRF cookie set"})
