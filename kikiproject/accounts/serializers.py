from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
)
from .models import CustomUser
from .emails import account_activation_token

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

        # html = render_to_string(
        #     "accounts/email_register.html",
        #     {
        #         "backend_base_url": settings.BACKEND_BASE_URL,
        #         "uidb64": urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
        #         "token": account_activation_token.make_token(user),
        #         "user": user,
        #     },
        # )
        # to_email = user.email
        # send_mail(
        #     "안녕하세요 키키입니다. 인증메일이 도착했어요!",
        #     "_",
        #     settings.DEFAULT_FROM_MAIL,
        #     [to_email],
        #     html_message=html,
        # )
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


class PublicUserSerializer(ModelSerializer):
    # is_host = SerializerMethodField()
    # total_bookmark_articles = SerializerMethodField()

    class Meta:
        model = CustomUser
        exclude = (
            "groups",
            "user_permissions",
            "password",
        )
    

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