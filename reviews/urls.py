from django.urls import include, path
from rest_framework.routers import DefaultRouter

from reviews.views import CommentViewSet, ReviewViewSet

# создаем роутер
v1_router = DefaultRouter()

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='ReviewsView'
)

v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='ReviewsView'
)
v1_router.register(
    r'titles/(P<titles_id>\.+)/(?P<review_id>.+)/comments',
    CommentViewSet,
    basename='CommentsView'
)


urlpatterns = [
    path('', include(v1_router.urls)),
]
