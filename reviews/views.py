from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review
from reviews.serializers import CommentSerializer, ReviewSerializer

from titles.models import Title

from users.permissions import IsAdminOrStaff


class ReviewViewSet(viewsets.ModelViewSet):
    """Модель обработки отзывов"""
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def serializing_and_rating_calculation(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, title=title)
        title.rating = (Review.objects.filter(title=title).aggregate(Avg(
            'score'))['score__avg'])
        title.save(update_fields=['rating'])

    def perform_create(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def perform_update(self, serializer):
        self.serializing_and_rating_calculation(serializer)

    def get_serializer_context(self):
        return {'title_id': self.kwargs['title_id'], 'request': self.request}


class CommentViewSet(viewsets.ModelViewSet):
    """Модель обработки комментариев"""
    serializer_class = CommentSerializer
    permission_classes = [IsAdminOrStaff, IsAuthenticatedOrReadOnly]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review

    def get_queryset(self):
        review = self.get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self.get_review()
        serializer.save(author=self.request.user, review=review)
