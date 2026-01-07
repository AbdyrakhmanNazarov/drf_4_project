from rest_framework.routers import DefaultRouter
from django.urls import path, include
from news.views import NewsViewSet, NewsCategoryViewSet, NewsTagViewSet

router = DefaultRouter()
router.register('news', NewsViewSet, basename='news')
router.register('news-category', NewsCategoryViewSet, basename='news-category')
router.register('news-tag', NewsTagViewSet, basename='news-tag')

urlpatterns = [
    path('', include(router.urls)),
]
