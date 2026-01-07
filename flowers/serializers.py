from rest_framework import serializers
from .models import Category, Tag, Flower, FlowerImage, Order, OrderItem


# ------------------ Category ------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


# ------------------ Tag ------------------
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


# ------------------ FlowerImage ------------------
class FlowerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerImage
        fields = ("id", "image")


# ------------------ Flower ------------------
class FlowerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    images = FlowerImageSerializer(many=True, read_only=True)  # inline images

    class Meta:
        model = Flower
        fields = (
            "id",
            "name",
            "description",
            "category",
            "tags",
            "price",
            "stock",
            "is_available",
            "created_at",
            "images",
        )


# ------------------ OrderItem ------------------
class OrderItemSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "flower", "quantity", "price", "total_price")


# ------------------ Order ------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "full_name",
            "phone",
            "address",
            "status",
            "created_at",
            "items",
            "total_price",
        )
