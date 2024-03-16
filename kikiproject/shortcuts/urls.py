from django.urls import path
from .views import (
    ShortcutKeyList, 
    ShortcutKeyDetail, 
    ProgramListView, 
    ShortcutKeyRank, 
    UpdateBookmarkAndRetrieveTop,
    ShortcutKeyFavoritesView,
    BookmarkProgram,
    BookmarkShortcut,
    CustomTokenRefreshView
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('shortcut-keys/', ShortcutKeyList.as_view(), name='shortcut-key-list'),
    path('shortcut-keys/allrank/', ShortcutKeyDetail.as_view(), name='shortcut-key-detail'),
    path('shortcut-keys/rank/', ShortcutKeyRank.as_view(), name='shortcut-key-rank'),
    path('shortcut-keys/programs/', ProgramListView.as_view(), name='program-list'),
    path('shortcut-keys/bookmark/', UpdateBookmarkAndRetrieveTop.as_view(), name='update-bookmark-retrieve-top'),
    path('shortcut-keys/bookmark/program/', BookmarkProgram.as_view(), name='bookmark-program'),
    path('shortcut-keys/bookmark/shortcut/', BookmarkShortcut.as_view(), name='bookmark-shortcut'),
    path('shortcut-keys/favorites/', ShortcutKeyFavoritesView.as_view(), name='read-favorites'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]
