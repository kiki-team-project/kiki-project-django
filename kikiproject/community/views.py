from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from community.models import Post, Comment
from rest_framework import viewsets
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer