from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "refresh": {
                        "type": "string",
                        "example": "eyJhbGciOiJIUzI1Ni..."
                    }
                },
                "required": [
                    "refresh"
                ]
            }
        },
        responses={
            200: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string"
                    }
                }
            },
            400: {
                "type": "object",
                "properties": {
                    "detail": {
                        "type": "string"
                    }
                }
            }
        }
    )

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]

            token = RefreshToken(refresh_token)

            token.blacklist()

            return Response(
                {"detail": "Вы успешно вышли из системы."},
                status=status.HTTP_200_OK
            )

        except KeyError:
            return Response(
                {"detail": "Refresh token обязателен."},
                status=status.HTTP_400_BAD_REQUEST
            )

        except TokenError:
            return Response(
                {"detail": "Недействительный токен."},
                status=status.HTTP_400_BAD_REQUEST
            )