from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import News, NewsCategory, NewsTag
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

User = get_user_model()

def create_test_image(filename="test.jpg"):
    image_io = BytesIO()
    img = Image.new('RGB', (100, 100), color=(0, 255, 0))
    img.save(image_io, 'JPEG')
    image_io.seek(0)
    return SimpleUploadedFile(filename, image_io.read(), content_type='image/jpeg')


class NewsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='12345',
            phone_number='+77001234567'
        )
        self.category = NewsCategory.objects.create(name="Новости IT", slug="it")
        self.tag = NewsTag.objects.create(name="Технологии", slug="tech")

        image_file = create_test_image()
        self.news = News.objects.create(
            title="Новая технология",
            content="Описание новости",
            category=self.category,
            image=image_file,
            is_published=True
        )
        self.news.tags.add(self.tag)

    def test_news_creation(self):
        self.assertEqual(self.news.title, "Новая технология")
        self.assertEqual(self.news.category.name, "Новости IT")
        self.assertIn(self.tag, self.news.tags.all())
