from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, OTPVerification
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils.timezone import now
import random
from .serializers import (
    RegisterSerializer,
    ProfileSerializer,
    LoginSerializer,
    GenericChangePasswordSerializer,
    DeactivateSerializer,
    ResetPasswordSerializer,
    VerifyPasswordResetOTPSerializer,
    SendResetPasswordSerializer,
)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(GenericAPIView):
    serializer_class = GenericChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({"message": "Пароль успешно изменён"})


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"message": "Вы вышли из системы"})


class DeactivateAccountView(GenericAPIView):
    serializer_class = DeactivateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not serializer.validated_data['confirm']:
            return Response({"error": "Подтвердите деактивацию"}, status=400)

        request.user.is_active = False
        request.user.save()
        return Response({"message": "Аккаунт деактивирован"})


class RequestPasswordResetView(GenericAPIView):
    serializer_class = SendResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email', None)
        if not email:
            return Response({"message": "Необходимо указать email"}, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            return Response({"message": "Пользователь с таким email не найден"}, status=status.HTTP_404_NOT_FOUND)

        code = str(random.randint(1000, 9999))

        OTPVerification.objects.update_or_create(
            email=email,
            defaults={'code': code, 'created_at': now()}
        )

        message = f"Ваш код для сброса пароля: {code}"
        response = send_mail(
            subject="Восстановление пароля",
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        if response == 0:
            return Response({"message": "Не удалось отправить код на email"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Код успешно отправлен на email"}, status=status.HTTP_200_OK)


class VerifyPasswordResetOTPView(GenericAPIView):
    serializer_class = VerifyPasswordResetOTPSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        code = serializer.validated_data['code']

        try:
            code_record = OTPVerification.objects.get(email=email, code=code)
            if code_record.is_expired():
                code_record.delete()
                return Response({"message": "Срок действия кода истек"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "Код успешно проверен"}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({"message": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        try:
            code_record = OTPVerification.objects.get(email=email, code=code)
            user = User.objects.get(email=email)

            if code_record.is_expired():
                code_record.delete()
                return Response({"message": "Срок действия кода истек"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            code_record.delete()
            return Response({"message": "Пароль успешно изменён"}, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({"message": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"message": "Пользователь не найден"}, status=status.HTTP_400_BAD_REQUEST)
