from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CategoryViewSet, PlatformViewSet, UserSpecificInfoView

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categorys', CategoryViewSet)
router.register(r'programs', PlatformViewSet)
#router.register(r'mypage', MyPageViewSet)

urlpatterns = [
    path('community/', include(router.urls)),
    path('mypage/token/', UserSpecificInfoView.as_view(), name='user-specific-info'),
]