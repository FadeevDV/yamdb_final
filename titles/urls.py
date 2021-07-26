from django.urls import include, path
from rest_framework.routers import DefaultRouter

from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

# создаем роутер
v1_router = DefaultRouter()
v1_router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)

v1_router.register(
    r'genres',
    GenreViewSet,
    basename='categories'
)

v1_router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)


urlpatterns = [
    path('', include(v1_router.urls)),
]
