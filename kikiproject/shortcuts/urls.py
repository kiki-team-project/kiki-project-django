from django.urls import path
from .views import ShortcutKeyList, ShortcutKeyDetail
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('shortcut-keys/', ShortcutKeyList.as_view(), name='shortcut-key-list'),
    path('shortcut-keys/<int:index>/', ShortcutKeyDetail.as_view(), name='shortcut-key-detail'),
]