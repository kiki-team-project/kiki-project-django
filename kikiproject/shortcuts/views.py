from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ShortcutKey, ProgramList
from .serializers import ShortcutKeySerializer, ProgramListSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404

class ShortcutKeyList(APIView):
    def get(self, request, format=None):
        platform = request.query_params.get('platform', None)

        if platform is not None:
            shortcuts = ShortcutKey.objects.filter(platform=platform)
        else:
            return Response({'error': 'Platform parameter is required'}, status=400)

        serializer = ShortcutKeySerializer(shortcuts, many=True)
        return Response(serializer.data)
    

# class ShortcutKeyDetail(APIView):

#     def get(self, request, index, format=None):
#         shortcut = ShortcutKey.objects.get(index=index)
#         shortcut.bookmark += 1
#         shortcut.save()
        
#         shortcut_keys = ShortcutKey.objects.all()[:5]  # 상위 5개 레코드 가져오기
#         serializer = ShortcutKeySerializer(shortcut_keys, many=True)
#         return Response(serializer.data)
    
class UpdateBookmarkAndRetrieveTop(APIView):
    def get(self, request, format=None):
        # Get the platform and id from query parameters
        platform = request.query_params.get('platform')
        id = request.query_params.get('id')

        if platform is None or id is None:
            return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Update the bookmark count
        shortcut = get_object_or_404(ShortcutKey, id=id, platform=platform)
        shortcut.bookmark += 1
        shortcut.save()

        # Retrieve top 5 shortcuts based on bookmark within the same platform
        top_shortcuts = ShortcutKey.objects.filter(platform=platform).order_by('-bookmark')[:5]
        serializer = ShortcutKeySerializer(top_shortcuts, many=True)

        return Response(serializer.data)
       
class ShortcutKeyRank(APIView):
    def get(self, request, format=None):
        platform = request.query_params.get('platform', None)

        if platform is not None:
            shortcuts = ShortcutKey.objects.filter(platform=platform).order_by('-bookmark')[:5]
        else:
            return Response({'error': 'Platform parameter is required'}, status=400)

        serializer = ShortcutKeySerializer(shortcuts, many=True)
        return Response(serializer.data)
    
    
class ProgramListView(APIView):
    def get(self, request, format=None):
        shortcuts = ProgramList.objects.all()
        serializer = ProgramListSerializer(shortcuts, many=True)
        return Response(serializer.data)