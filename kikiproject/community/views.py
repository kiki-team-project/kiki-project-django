from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, PlatformSerializer
from community.models import Post, Comment, CategoryList, PlatformList
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # 사용자 정의 응답
        return Response({
            "message": "success",
            "post": serializer.data
        }, status=status.HTTP_201_CREATED)
        
    def get_queryset(self):
        """
        Optionally restricts the returned posts to a given category or platform,
        by filtering against query parameters in the URL.
        """
        queryset = Post.objects.all()
        category = self.request.query_params.get('category', None)
        platform = self.request.query_params.get('platform', None)

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
        
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def create(self, request, *args, **kwargs):
        print(request.data)
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
    
