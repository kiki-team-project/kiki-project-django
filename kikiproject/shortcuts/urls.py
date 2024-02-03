from django.urls import path
from .views import (
    ShortcutKeyList, 
    ShortcutKeyDetail, 
    ProgramListView, 
    ShortcutKeyRank, 
    UpdateBookmarkAndRetrieveTop,
    ShortcutKeyFavoritesView
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('shortcut-keys/', ShortcutKeyList.as_view(), name='shortcut-key-list'),
    path('shortcut-keys/allrank/', ShortcutKeyDetail.as_view(), name='shortcut-key-detail'),
    path('shortcut-keys/rank/', ShortcutKeyRank.as_view(), name='shortcut-key-rank'),
    path('shortcut-keys/programs/', ProgramListView.as_view(), name='program-list'),
    path('shortcut-keys/bookmark/', UpdateBookmarkAndRetrieveTop.as_view(), name='update-bookmark-retrieve-top'),
    path('shortcut-keys/favorites/', ShortcutKeyFavoritesView.as_view(), name='read-favorites'),
]
