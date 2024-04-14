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

        user = CustomUser.objects.create_user(**validated_data)
        return user
    
    def validate(self, attrs): # 중복 체크
        username = attrs['username']
        nickname = attrs['nickname']
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("user already exists")
        if nickname == "":
            raise serializers.ValidationError("nickname is required")
        if CustomUser.objects.filter(nickname=nickname).exists():
            raise serializers.ValidationError("nickname already exists")
        return attrs
    
    os_type = serializers.ChoiceField(choices=CustomUser.OSTypechoices.choices, required=True)
    year_type = serializers.ChoiceField(choices=CustomUser.YearTypeChoices.choices, required=True)
    job_type = serializers.ChoiceField(choices=CustomUser.JobTypeChoices.choices, required=True)
    def validate_type(self, value):
        choices_dict = {
            'OSType': CustomUser.OSTypechoices.choices,
            'YearType': CustomUser.YearTypeChoices.choices,
            'JobType': CustomUser.JobTypeChoices.choices
        }
        for field, choices in choices_dict.items():
            if value not in dict(choices).keys():
                raise serializers.ValidationError(f"Invalid {field}")

    

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
    
    def validate(self, data):
        # 필요한 필드(ostype, yeartype)가 모두 비어있을 경우 오류 반환
        if not any(data.values()):
            raise serializers.ValidationError("At least one field (ostype, yeartype, jobtype) must be provided.")
        return data
    

class CustomUserSerializer(serializers.ModelSerializer):
    os_type = serializers.ChoiceField(choices=CustomUser.OSTypechoices.choices, required=True)
    year_type = serializers.ChoiceField(choices=CustomUser.YearTypeChoices.choices, required=True)
    job_type = serializers.ChoiceField(choices=CustomUser.JobTypeChoices.choices, required=True)
    def validate_ostype(self, value):
        if value not in dict(CustomUser.OSTypechoices.choices).keys():
            raise serializers.ValidationError("Invalid OSType")
        return value

    def validate_yeartype(self, value):
        if value not in dict(CustomUser.YearTypeChoices.choices).keys():
            raise serializers.ValidationError("Invalid YearType")
        return value
    
    def validate_jobtype(self, value):
        if value not in dict(CustomUser.JobTypeChoices.choices).keys():
            raise serializers.ValidationError("Invalid JobType")
        return value

    class Meta:
        model = CustomUser
        fields = "__all__"


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