from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ShortcutKey
from .serializers import ShortcutKeySerializer
from django.http import Http404

class ShortcutKeyList(APIView):
    def get(self, request, format=None):
        shortcuts = ShortcutKey.objects.all()
        serializer = ShortcutKeySerializer(shortcuts, many=True)
        return Response(serializer.data)
    

class ShortcutKeyDetail(APIView):

    def get(self, request, index, format=None):
        shortcut = ShortcutKey.objects.get(index=index)
        shortcut.bookmark += 1
        shortcut.save()
        
        shortcut_keys = ShortcutKey.objects.all()[:5]  # 상위 5개 레코드 가져오기
        serializer = ShortcutKeySerializer(shortcut_keys, many=True)
        return Response(serializer.data)