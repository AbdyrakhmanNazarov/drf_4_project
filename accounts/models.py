from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from django.utils.timezone import now

class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-date_joined",)

    ROLE_CHOICES = (
        ("user", "Пользователь"),
        ("admin", "Администратор"),
    )

    username = None

    email = models.EmailField(verbose_name="электронная почта", unique=True)
    phone_number = PhoneNumberField(verbose_name="Номер телефона", blank=True, null=True)
    full_name = models.CharField(max_length=200, verbose_name="ФИО", blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user", verbose_name="Роль пользователя")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return self.email or str(self.phone_number)


class OTPVerification(models.Model):
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def is_expired(self):
        # Время жизни кода 5 минут (300 секунд)
        return (now() - self.created_at).total_seconds() > 300

    def __str__(self):
        return f"{self.email} - {self.code}"
