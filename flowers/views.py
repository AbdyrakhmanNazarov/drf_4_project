from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category, Tag, Flower, Order
from .serializers import CategorySerializer, TagSerializer, FlowerSerializer, OrderSerializer
from .paginations import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly


# ------------------ Category ------------------
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]


# ------------------ Tag ------------------
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]


# ------------------ Flower ------------------
class FlowerViewSet(viewsets.ModelViewSet):
    queryset = Flower.objects.all().order_by('-created_at')
    serializer_class = FlowerSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]


# ------------------ Order ------------------
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdminOrReadOnly]





# # Второй вариант
# from rest_framework import generics, permissions
# from .models import Category, Tag, Flower, FlowerImage, Order, OrderItem
# from .serializers import (
#     CategorySerializer,
#     TagSerializer,
#     FlowerSerializer,
#     OrderSerializer,
# )
# from .paginations import StandardResultsSetPagination
# from .permissions import IsAdminOrReadOnly

# # ------------------ Category ------------------
# class CategoryListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAdminOrReadOnly]


# class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [IsAdminOrReadOnly]


# # ------------------ Tag ------------------
# class TagListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAdminOrReadOnly]


# class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [IsAdminOrReadOnly]


# # ------------------ Flower ------------------
# class FlowerListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Flower.objects.all().order_by('-created_at')
#     serializer_class = FlowerSerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAdminOrReadOnly]


# class FlowerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Flower.objects.all()
#     serializer_class = FlowerSerializer
#     permission_classes = [IsAdminOrReadOnly]


# # ------------------ Order ------------------
# class OrderListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Order.objects.all().order_by('-created_at')
#     serializer_class = OrderSerializer
#     pagination_class = StandardResultsSetPagination
#     permission_classes = [IsAdminOrReadOnly]


# class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAdminOrReadOnly]
