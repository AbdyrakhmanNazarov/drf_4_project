from django.db import models
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Flower(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="flowers"
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="flowers",
        blank=True
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Цветок"
        verbose_name_plural = "Цветы"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class FlowerImage(models.Model):
    flower = models.ForeignKey(
        Flower,
        related_name="images",
        on_delete=models.CASCADE
    )

    image = ResizedImageField(
        size=[800, 800],
        crop=['middle', 'center'],
        quality=85,
        upload_to="flowers/"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображение цветка"
        verbose_name_plural = "Изображения цветков"

    def __str__(self):
        return f"Image for {self.flower.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ("new", "Новый"),
        ("paid", "Оплачен"),
        ("sent", "Отправлен"),
        ("done", "Завершён"),
        ("canceled", "Отменён"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.id}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    flower = models.ForeignKey(
        Flower,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.flower.name} × {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.price
