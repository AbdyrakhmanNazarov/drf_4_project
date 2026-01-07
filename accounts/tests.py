from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User, OTPVerification
from django.utils.timezone import now
import random


class UserAuthTests(APITestCase):
    def setUp(self):
        # создаём тестового пользователя
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='strongpassword123',
            full_name='Тест Пользователь',
            phone_number='+77001234567'  # необязательно, можно None
        )

    def get_jwt_tokens(self, email='testuser@example.com', password='strongpassword123'):
        """Возвращает access и refresh токены"""
        url = reverse('login')
        data = {'email': email, 'password': password}
        response = self.client.post(url, data, format='json')
        return response.data['access'], response.data['refresh']

    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'full_name': 'Новый Пользователь',
            'password': 'newpassword123',
            'phone_number': '+77009876543'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_user_without_phone(self):
        url = reverse('register')
        data = {
            'email': 'nopho@example.com',
            'full_name': 'Без телефона',
            'password': 'nopassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='nopho@example.com').exists())

    def test_login_user(self):
        url = reverse('login')
        data = {'email': 'testuser@example.com', 'password': 'strongpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_profile_access(self):
        access_token, _ = self.get_jwt_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_change_password(self):
        access_token, _ = self.get_jwt_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('change-password')
        data = {'old_password': 'strongpassword123', 'new_password': 'newstrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверяем, что новый пароль работает
        response = self.client.post(reverse('login'),
                                    {'email': 'testuser@example.com', 'password': 'newstrongpassword'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deactivate_account(self):
        access_token, _ = self.get_jwt_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('deactivate')
        data = {'confirm': True}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_logout(self):
        access_token, refresh_token = self.get_jwt_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        url = reverse('logout')
        data = {'refresh': refresh_token}  # реальный refresh токен
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_flow(self):
        # Генерируем OTP
        code = str(random.randint(1000, 9999))
        OTPVerification.objects.create(email=self.user.email, code=code, created_at=now())

        # Проверка OTP
        url_verify = reverse('verify-password-reset')
        response = self.client.post(url_verify, {'email': self.user.email, 'code': code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сброс пароля
        url_reset = reverse('complete-password-reset')
        response = self.client.post(
            url_reset,
            {'email': self.user.email, 'code': code, 'new_password': 'resetpass123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Логин с новым паролем
        response = self.client.post(reverse('login'), {'email': self.user.email, 'password': 'resetpass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
