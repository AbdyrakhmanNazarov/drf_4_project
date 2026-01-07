from rest_framework import mixins, viewsets
from .models import News, NewsCategory, NewsTag
from .serializers import NewsSerializer, NewsCategorySerializer, NewsTagSerializer
from .permissions import IsAdmin
from .paginations import StandardResultsSetPagination

class NewsCategoryViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    queryset = NewsCategory.objects.all()
    serializer_class = NewsCategorySerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdmin]


class NewsTagViewSet(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = NewsTag.objects.all()
    serializer_class = NewsTagSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdmin]


class NewsViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAdmin]
