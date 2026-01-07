from django.db import models
from django_resized import ResizedImageField


class NewsCategory(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категория новости"
        verbose_name_plural = "Категории новостей"
        ordering = ["name"]

    def __str__(self):
        return self.name


class NewsTag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        verbose_name = "Тег новости"
        verbose_name_plural = "Теги новостей"
        ordering = ["name"]

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(
        NewsCategory, on_delete=models.CASCADE, related_name="news"
    )
    tags = models.ManyToManyField(NewsTag, related_name="news", blank=True)
    image = ResizedImageField(
        size=[800, 800],
        crop=['middle', 'center'],
        quality=85,
        upload_to="news/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
