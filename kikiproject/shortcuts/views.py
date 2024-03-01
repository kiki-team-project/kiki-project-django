from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import ShortcutKey, ProgramList
from .serializers import ShortcutKeySerializer, ProgramListSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.models import User

class ShortcutKeyList(APIView):
    def get(self, request, format=None):
        platform = request.query_params.get('platform', None)

        if platform is not None:
            shortcuts = ShortcutKey.objects.filter(platform=platform)
        else:
            return Response({'error': 'Platform parameter is required'}, status=400)

        serializer = ShortcutKeySerializer(shortcuts, many=True)
        return Response(serializer.data)
    

class ShortcutKeyDetail(APIView):

    def get(self, request, format=None):
        
        shortcut_keys = ShortcutKey.objects.all()[:5]  # 상위 5개 레코드 가져오기
        serializer = ShortcutKeySerializer(shortcut_keys, many=True)
        return Response(serializer.data)
    
class UpdateBookmarkAndRetrieveTop(APIView):
    
    def get(self, request, format=None):        

        try:
            platform = request.query_params.get('platform')
            id = request.query_params.get('id')

            if platform is None or id is None:
                return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            # Update the bookmark count
            shortcut = get_object_or_404(ShortcutKey, id=id, platform=platform)
            shortcut.bookmark += 1
            shortcut.save()
            # Retrieve top 5 shortcuts based on bookmark within the same platform
            # top_shortcuts = ShortcutKey.objects.filter(platform=platform).order_by('-bookmark')[:5]
            # serializer = ShortcutKeySerializer(top_shortcuts, many=True)
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
       
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
        serializer = ProgramListSerializer(shortcuts, many=True, context={'request': request})
        return Response(serializer.data)
    
    
class ShortcutKeyFavoritesView(APIView):
    """
    클라이언트로부터 받은 id_list에 해당하는 ShortcutKey 인스턴스들을 반환합니다.
    """

    def post(self, request, *args, **kwargs):
        id_list = request.data.get('id_list', [])
        
        # id_list에 해당하는 ShortcutKey 인스턴스들을 조회
        shortcuts = ShortcutKey.objects.filter(id__in=id_list)
        
        # 직렬화
        serializer = ShortcutKeySerializer(shortcuts, many=True)
        
        # JSON 응답 반환
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookmarkShortcut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            platform = request.query_params.get('platform')
            shortcut_id = request.query_params.get('shortcut_id')

            if platform is None or shortcut_id is None:
                return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = userinfo.bookmark_shortcut.split()
            
            if shortcut_id not in infolist:
                # Update the bookmark count
                shortcut = get_object_or_404(ShortcutKey, id=shortcut_id, platform=platform)
                shortcut.bookmark += 1
                shortcut.save()
                
                infolist.append(shortcut_id)
                

            userinfo.bookmark_shortcut = " ".join(infolist)
            userinfo.save()
            print("info :", infolist)
            # Retrieve top 5 shortcuts based on bookmark within the same platform
            # top_shortcuts = ShortcutKey.objects.filter(platform=platform).order_by('-bookmark')[:5]
            # serializer = ShortcutKeySerializer(top_shortcuts, many=True)
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):

        try:
            
            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = userinfo.bookmark_shortcut.split()

            userinfo.bookmark_shortcut = " ".join(infolist)
            userinfo.save()
            shortcuts = ShortcutKey.objects.filter(id__in=infolist)

            # 직렬화
            serializer = ShortcutKeySerializer(shortcuts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):

        try:
            platform = request.query_params.get('platform')
            shortcut_id = request.query_params.get('shortcut_id')

            if platform is None or shortcut_id is None:
                return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = []
            for info in userinfo.bookmark_shortcut.split():
                if info != shortcut_id:
                    infolist.append(info)
                    
                else:
                    # Update the bookmark count
                    shortcut = get_object_or_404(ShortcutKey, id=shortcut_id, platform=platform)
                    shortcut.bookmark -= 1
                    shortcut.save()

            userinfo.bookmark_shortcut = " ".join(infolist)
            userinfo.save()
            print("info :", infolist)
            # 삭제 후 성공 응답 반환
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
    
    
class BookmarkProgram(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        try:
            platform = request.query_params.get('platform')
            program_id = request.query_params.get('program_id')

            if platform is None or program_id is None:
                return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = userinfo.bookmark_program.split()
            
            if program_id not in infolist:
                # Update the bookmark count
                program = get_object_or_404(ProgramList, id=program_id, platform=platform)
                program.bookmark += 1
                program.save()
               
                infolist.append(program_id)

            userinfo.bookmark_program = " ".join(infolist)
            userinfo.save()
            print("info :", infolist)
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):

        try:
            
            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = userinfo.bookmark_program.split()

            shortcuts = ProgramList.objects.filter(id__in=infolist)
            print(shortcuts)
            # 직렬화
            serializer = ProgramListSerializer(shortcuts, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):

        try:
            platform = request.query_params.get('platform')
            program_id = request.query_params.get('program_id')

            if platform is None or program_id is None:
                return Response({"error": "Platform and ID must be provided."}, status=status.HTTP_400_BAD_REQUEST)

            user = request.user
            userinfo = User.objects.filter(username=user).first()
            infolist = []
            for info in userinfo.bookmark_program.split():
                
                if info != program_id:
                    infolist.append(info)
                
                else:
                    # Update the bookmark count
                    program = get_object_or_404(ProgramList, id=program_id, platform=platform)
                    program.bookmark -= 1
                    program.save()
                    
            userinfo.bookmark_program = " ".join(infolist)
            userinfo.save()
            print("info :", infolist)
            # 삭제 후 성공 응답 반환
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
        
        
# class UserSpecificInfoView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         user = request.user
#         print("useruseruser : ", user)
#         post_queryset = Post.objects.all()
#         user_id = user.id
        
#         post_queryset = post_queryset.filter(author=user)
#         print(post_queryset)
        
#         user_info = {
#             "id": user.id,
#             "username": user.username,
#             "nickname": user.nickname,
#             "photo": user.photo,
#             "login_type": user.login_type,
#         }
#         serializer = PostSerializer(post_queryset, many=True)  # Serialize the queryset
#         return Response(serializer.data)  # Return a DRF `Response` object
#         #return post_queryset