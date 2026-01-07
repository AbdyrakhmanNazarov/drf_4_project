from rest_framework import serializers
from .models import News, NewsCategory, NewsTag

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ("id", "name", "slug")


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ("id", "name", "slug")


class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer(read_only=True)
    tags = NewsTagSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ("id", "title", "content", "category", "tags", "image", "is_published", "created_at")
