"""Views for Users."""

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)

from core.token_authentication import JWTAuthentication
from core.serializers.user import (
    UserListSerializer,
    UserDetailSerializer,
    UserRegistrationSerializer,
    MeSerializer,
    LoginSerializer,
)

User = get_user_model()


class UserList(ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserListSerializer
    queryset = User().get_all_actives()


class UserDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = UserDetailSerializer
    queryset = User().get_all_actives()
    lookup_field = "uid"


class UserRegistration(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    queryset = User().get_all_actives()


class MeDetail(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user


@api_view(["POST"])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        token = JWTAuthentication.generate_token(payload=serializer.data)
        return Response(
            {"message": "Login Success", "token": token, "user": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = JWTAuthentication.generate_token(payload=serializer.data)
            return Response(
                {"message": "Login Success", "token": token, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginGeneric(CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = JWTAuthentication.generate_token(payload=serializer.data)
            return Response(
                {"message": "Login Success", "token": token, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
