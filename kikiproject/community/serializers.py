from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, CategoryList, PlatformList

User = get_user_model()

class UserEmailField(serializers.Field):
    def to_internal_value(self, data):
        try:
            return User.objects.get(email=data)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist")

    def to_representation(self, value):
        return value.email

class PostSerializer(serializers.ModelSerializer):
    author = UserEmailField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'category', 'platform', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    author = UserEmailField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'content', 'created_at']
        
        
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryList
        fields = ['category']
        
        
class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformList
        fields = ['platform']