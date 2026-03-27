from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import UpdateAPIView, GenericAPIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    SignUpSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)

User = get_user_model()


# ================== SIGNUP ==================
class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                'status': status.HTTP_201_CREATED,
                'message': f"{user.username} muvaffaqiyatli royxatdan otdi"
            },
            status=status.HTTP_201_CREATED
        )


# ================== LOGIN ==================
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'message': 'Username yoki parol notogri'},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )


# ================== LOGOUT ==================
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response(
                {'message': 'Refresh token yuborilmadi'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Logout successful'},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception:
            return Response(
                {'message': 'Token xato yoki eskirgan'},
                status=status.HTTP_400_BAD_REQUEST
            )


# ================== PROFILE ==================
class UserProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)


# ================== UPDATE ==================
class UserUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # javob qaytarish
        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Malumot muvaffaqiyatli tahrirlandi",
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )


# ================== CHANGE PASSWORD ==================
class ChangePasswordView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        serializer.update(self.get_object(), serializer.validated_data)

        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Parol muvaffaqiyatli o‘zgartirildi"
            },
            status=status.HTTP_200_OK
        )