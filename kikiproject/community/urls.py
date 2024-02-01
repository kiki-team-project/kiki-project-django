from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CategoryViewSet, PlatformViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'programs', PlatformViewSet)


urlpatterns = [
    path('community/', include(router.urls)),
]