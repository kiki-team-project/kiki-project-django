from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import (
    ModelSerializer,
)
from .models import CustomUser

class UserSerializer(ModelSerializer):
    # is_host = SerializerMethodField()
    # total_bookmark_articles = SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = (
            "groups",
            "user_permissions",
        )
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def validate(self, attrs): # 중복 체크
        username = attrs['username']
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("user already exists")
        return attrs
    
    def validate_username(self, value):
        try:
            # 이메일 형식인지 확인
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        return value
    

class UserDetailSerializer(ModelSerializer):
    # is_host = SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = (
            "groups",
            "user_permissions",
        )
        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
        }


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["id"] = user.id
        token["username"] = user.username
        token["login_type"] = user.login_type
        return token
    

class UserProfilePhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['photo']