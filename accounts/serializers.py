from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        phone = data.get('phone_number', None)
        password = data['password']

        if not email and not phone:
            raise serializers.ValidationError("Укажите email или телефон для входа")

        user = None
        if email:
            user = authenticate(email=email, password=password)
        elif phone:
            user = authenticate(phone_number=phone, password=password)

        if not user:
            raise serializers.ValidationError("Неверные данные для входа")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт неактивен")

        refresh = RefreshToken.for_user(user)
        return {
            'user_id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'full_name', 'role')


class GenericChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Неверный старый пароль")
        return value


class DeactivateSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()


class SendResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)


class VerifyPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=4)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(write_only=True, min_length=6)
