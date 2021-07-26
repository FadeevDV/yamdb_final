from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from titles.filters import TitleFilter
from titles.models import Category, Genre, Title
from titles.serializers import (CategorySerializer, GenreSerializer,
                                TitleSerializer_NOTSAFE, TitleSerializer_SAFE)
from users.permissions import IsAdminOrReadOnly


class CategoryViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """Операции с категориями произведений"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def delete(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        category.delete()
        return Response(status.HTTP_200_OK, status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    '''Операции с жанрами произведений'''
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def delete(self, request, slug):
        genre = get_object_or_404(Genre, slug=slug)
        genre.delete()
        return Response(status.HTTP_200_OK, status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    '''Операции с произведениями'''
    queryset = Title.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        safe_methods = ['list', 'retrieve']
        print(self.action)
        if self.action in safe_methods:
            return TitleSerializer_SAFE
        return TitleSerializer_NOTSAFE
