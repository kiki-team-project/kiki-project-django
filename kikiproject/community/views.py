from .serializers import PostSerializer, CommentSerializer, CategorySerializer, PlatformSerializer
from community.models import Post, Comment, CategoryList, PlatformList
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(data)
    
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                "message": "success",
                "post": serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # 유효성 검사 실패 시, 에러 메시지 로깅
            print("Validation errors:", serializer.errors)
            # 클라이언트에게 에러 메시지 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer.is_valid(raise_exception=True)
        # #serializer.is_valid(raise_exception=True)
        # print("serializer :", serializer)
        # self.perform_create(serializer)
        # # 사용자 정의 응답
        # return Response({
        #     "message": "success",
        #     "post": serializer.data
        # }, status=status.HTTP_201_CREATED)
        
    def get_queryset(self):

        queryset = Post.objects.all()
        post_id = self.request.query_params.get('id', None)
        category = self.request.query_params.get('category', None)
        platform = self.request.query_params.get('platform', None)

        if post_id is not None:
            queryset = queryset.filter(id=post_id)
        if category is not None:
            queryset = queryset.filter(category=category)
        if platform is not None:
            queryset = queryset.filter(platform=platform)

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({
            "message": "success",
            "post": serializer.data
        }, status=status.HTTP_200_OK)


class UserSpecificInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_info = {
            "id": user.id,
            "username": user.username,
            "login_type": user.login_type,
        }
        return Response({
            "message": "success",
            "user": user_info
        }, status=status.HTTP_200_OK)
# class MyPageViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     pagination_class = CustomPagination
    
#     def get_queryset(self):

#         queryset = Post.objects.all()
#         token = self.request.query_params.get('token', None)

#         if token is not None:
#             queryset = queryset.filter(id=token)
            
#         return queryset
    
    
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 사용자 정의 응답
        return Response({
            "message": "success",
            "comment": serializer.data
        }, status=status.HTTP_201_CREATED)
        
    def get_queryset(self):
        queryset = Comment.objects.all()
        comment_id = self.request.query_params.get('id')
        post_id = self.request.query_params.get('post')

        if comment_id is not None:
            queryset = queryset.filter(id=comment_id)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)

        return queryset
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "success", "code" : 0}, status=status.HTTP_200_OK)
        except Exception as e:
            # Log the exception if needed
            return Response({"message": "fail", "code" : -1}, status=status.HTTP_400_BAD_REQUEST)

    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CategoryList.objects.all()
    serializer_class = CategorySerializer


class PlatformViewSet(viewsets.ModelViewSet):
    queryset = PlatformList.objects.all()
    serializer_class = PlatformSerializer
    
