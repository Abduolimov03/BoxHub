from drf_spectacular.utils import extend_schema
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from apps.models import User
from apps.pagination import StandardResultsSetPagination
from apps.serializers import LoginModelSerializer, RegisterModelSerializer, UserModelSerializer


@extend_schema(
    tags=["Users"],
    description="Ro'yhatdan o'tgan Foydalanuvchilar",
    request=UserModelSerializer,
)
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination


@extend_schema(
    tags=["Auth"],
    description="Foydalanuvchini email orqali ro'yhatdan o'tdi.",
    request=RegisterModelSerializer,
)
class RegisterAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "Foydalanuvchi muvaffaqiyatli ro'yxatdan o'tdi.",
                "user": {
                    "id": user.id,
                    "phone_number": user.phone_number,
                    "full_name": f"{user.first_name} {user.last_name}",
                    "is_active": user.is_active,
                }
            },
            status=HTTP_201_CREATED
        )


@extend_schema(
    tags=["Auth"],
    description="Foydalanuvchini telefon raqami orqali tizimga kiritish.",
    request=LoginModelSerializer,
)
class LoginAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginModelSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = RefreshToken.for_user(user)
        if not user.is_active:
            user.is_active = True
            user.save()

        return Response(
            {
                "access": str(tokens.access_token),
                "refresh": str(tokens),
            },
            status=HTTP_200_OK
        )
