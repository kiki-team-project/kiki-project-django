from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post, Comment, CategoryList, PlatformList

User = get_user_model()

# class UserEmailField(serializers.Field):
#     def to_internal_value(self, data):
#         try:
#             return User.objects.get(email=data)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User with this email does not exist")

#     def to_representation(self, value):
#         return value.email
    
class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'content', 'like_post', 'category', 'platform', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # context에서 request 객체를 가져옵니다.
        user = self.context['request'].user
        nick_name = user.nickname
        # request에서 추출한 사용자를 author로 사용하여 Post 인스턴스를 생성합니다.
        post = Post.objects.create(**validated_data, author=user, nickname=nick_name)
        return post

class CommentSerializer(serializers.ModelSerializer):
    #author = UserEmailField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'like_post', 'content', 'created_at']
        
        
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryList
        fields = ['category']
        
        
class PlatformSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformList
        fields = ['platform']
