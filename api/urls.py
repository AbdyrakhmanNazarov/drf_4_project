from django.urls import path, include

urlpatterns = [
    path('', include('api.yasg')),
    path('auth/', include('api.endpoints_accounts')),
    path('flowers/', include('api.endpoints_flowers')),
    path('news/', include('api.endpoints_news')),
]