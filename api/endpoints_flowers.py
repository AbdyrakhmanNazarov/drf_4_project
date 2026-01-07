from rest_framework.routers import DefaultRouter
from django.urls import path, include
from flowers.views import CategoryViewSet, TagViewSet, FlowerViewSet, OrderViewSet

# создаём router
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('tags', TagViewSet, basename='tags')
router.register('flowers', FlowerViewSet, basename='flowers')
router.register('orders', OrderViewSet, basename='orders')

# подключаем router к URL
urlpatterns = [
    path('', include(router.urls)),
]


# # Второй вариант
# from django.urls import path
# from flowers.views import (
#     CategoryListCreateAPIView,
#     CategoryRetrieveUpdateDestroyAPIView,
#     TagListCreateAPIView,
#     TagRetrieveUpdateDestroyAPIView,
#     FlowerListCreateAPIView,
#     FlowerRetrieveUpdateDestroyAPIView,
#     OrderListCreateAPIView,
#     OrderRetrieveUpdateDestroyAPIView,
# )

# urlpatterns = [
#     # Categories
#     path("categories/", CategoryListCreateAPIView.as_view(), name="category-list"),
#     path("categories/<int:pk>/", CategoryRetrieveUpdateDestroyAPIView.as_view(), name="category-detail"),

#     # Tags
#     path("tags/", TagListCreateAPIView.as_view(), name="tag-list"),
#     path("tags/<int:pk>/", TagRetrieveUpdateDestroyAPIView.as_view(), name="tag-detail"),

#     # Flowers
#     path("flowers/", FlowerListCreateAPIView.as_view(), name="flower-list"),
#     path("flowers/<int:pk>/", FlowerRetrieveUpdateDestroyAPIView.as_view(), name="flower-detail"),

#     # Orders
#     path("orders/", OrderListCreateAPIView.as_view(), name="order-list"),
#     path("orders/<int:pk>/", OrderRetrieveUpdateDestroyAPIView.as_view(), name="order-detail"),
# ]
# #