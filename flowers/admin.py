from django.contrib import admin
from .models import Category, Tag, Flower, FlowerImage, Order, OrderItem


# ------------------ Category ------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "created_at")
    list_display_links = ("id", "name")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


# ------------------ Tag ------------------
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_display_links = ("id", "name")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)


# ------------------ FlowerImage Inline ------------------
class FlowerImageInline(admin.TabularInline):
    model = FlowerImage
    extra = 1       # сколько пустых полей отображать по умолчанию
    min_num = 1     # минимум одно изображение
    max_num = 5     # максимум 5 изображений
    readonly_fields = ("created_at",)
    fields = ("image", "created_at")


# ------------------ Flower ------------------
@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "stock", "is_available", "created_at")
    list_display_links = ("id", "name")
    list_filter = ("category", "is_available", "created_at")
    search_fields = ("name", "description")
    inlines = [FlowerImageInline]
    ordering = ("-created_at",)


# ------------------ OrderItem Inline ------------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("total_price",)


# ------------------ Order ------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "phone", "status", "created_at", "total_price")
    list_display_links = ("id", "full_name")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone")
    inlines = [OrderItemInline]
    readonly_fields = ("created_at", "total_price")
    ordering = ("-created_at",)
