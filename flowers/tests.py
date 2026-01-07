from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Tag, Flower, FlowerImage, Order, OrderItem
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()


class CategoryTagTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Розы", slug="rozy")
        self.tag = Tag.objects.create(name="Красные", slug="krasnye")

    def test_category_creation(self):
        self.assertEqual(self.category.name, "Розы")
        self.assertEqual(self.category.slug, "rozy")

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, "Красные")
        self.assertEqual(self.tag.slug, "krasnye")


class FlowerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Розы", slug="rozy")
        self.tag = Tag.objects.create(name="Красные", slug="krasnye")
        self.flower = Flower.objects.create(
            name="Красная роза",
            description="Красная роза 50 см",
            category=self.category,
            price=10.50,
            stock=5,
            is_available=True
        )
        self.flower.tags.add(self.tag)

        # создаём корректное изображение в памяти
        image_io = io.BytesIO()
        image = Image.new("RGB", (10, 10), color=(255, 0, 0))  # маленькое красное изображение
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        image_file = SimpleUploadedFile(
            "test.jpg", image_io.read(), content_type="image/jpeg"
        )
        self.image = FlowerImage.objects.create(
            flower=self.flower,
            image=image_file
        )

    def test_flower_creation(self):
        self.assertEqual(self.flower.name, "Красная роза")
        self.assertEqual(self.flower.category.name, "Розы")
        self.assertIn(self.tag, self.flower.tags.all())
        self.assertTrue(self.flower.is_available)

    def test_flower_image(self):
        self.assertEqual(self.flower.images.count(), 1)
        image_file = self.flower.images.first().image

        # проверяем, что файл реально есть
        self.assertTrue(bool(image_file))

        # проверяем, что имя содержит 'test'
        self.assertIn("test", image_file.name.lower())

        # проверяем, что расширение корректное
        self.assertTrue(image_file.name.lower().endswith((".jpg", ".jpeg")))


class OrderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="testuser@example.com", password="12345", phone_number="+77001112233")
        self.category = Category.objects.create(name="Розы", slug="rozy")
        self.flower = Flower.objects.create(
            name="Красная роза",
            category=self.category,
            price=10.50,
            stock=5
        )

        self.order = Order.objects.create(
            user=self.user,
            full_name="Иван Иванов",
            phone="+77001112233",
            address="г. Алматы, ул. Цветочная 1",
            status="new"
        )

        self.order_item = OrderItem.objects.create(
            order=self.order,
            flower=self.flower,
            quantity=2,
            price=self.flower.price
        )

    def test_order_creation(self):
        self.assertEqual(self.order.full_name, "Иван Иванов")
        self.assertEqual(self.order.status, "new")
        self.assertEqual(self.order.items.count(), 1)

    def test_order_total_price(self):
        self.assertEqual(self.order.total_price, 21.0)
