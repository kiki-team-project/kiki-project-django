import requests

from django.conf import settings
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import (
    PermissionDenied,
)
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import (
    UserSerializer,
    UserDetailSerializer,
    CustomTokenObtainPairSerializer,
    UserProfilePhotoUpdateSerializer
)
from accounts import serializers
from accounts.models import CustomUser

# Create your views here.
class UserView(APIView):
    '''
    get : 유저 전체 보기
    post : 회원가입 과정
        조건 통과 시 UserSerializer 거쳐서 회원가입됨
    '''

    def get(self, request):
        user = CustomUser.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        password2 = request.data.get("second_password")
        nickname = request.data.get("nickname")
        if not password or not password2:
            return Response(
                {"error": "비밀번호 입력은 필수입니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not username:
            return Response(
                {"error": "이메일 입력은 필수입니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not nickname:
            return Response(
                {"error": "닉네임 입력은 필수입니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if password != password2:
            return Response(
                {"error": "비밀번호가 일치하지 않습니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"error": "해당 이메일을 가진 유저가 이미 있습니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if CustomUser.objects.filter(nickname=nickname).exists():
            return Response(
                {"error": "해당 닉네임을 가진 유저가 이미 있습니다!"}, status=status.HTTP_400_BAD_REQUEST
            )
        if len(password) < 6:
            return Response(
                {"error": "비밀번호는 6자리 이상이어야 합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(nickname) > 10 or len(nickname) < 2:
            return Response(
                {"error": "닉네임은 2자리 이상, 10자리 이하입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = UserSerializer(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid():
            newuser = serializer.save()
            response = Response({"message": "register success"},status=status.HTTP_201_CREATED)
            if newuser:
                return response
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        

class LoginView(TokenObtainPairView):
    '''
    TokenObtainPairView를 커스터마이징함
    '''
    serializer_class = CustomTokenObtainPairSerializer


# Create your views here.
class LoginView(TokenObtainPairView):
    '''
    TokenObtainPairView를 커스터마이징함
    '''
    serializer_class = CustomTokenObtainPairSerializer


class KakaoLoginView(APIView):
    '''
    카카오 소셜로그인 함수
    Post 함수 원리 
    1. 클라이언트가 전송한 요청 데이터에서 "code" 필드를 가져옵니다. 이 코드는 카카오 OAuth 인증 시스템에서 발급한 인증 코드입니다.
    2. 카카오 토큰을 얻기 위한 API 엔드포인트 URL을 지정합니다.
    3. data = { ... }: 카카오 API로 전송할 데이터를 구성합니다. 여기에는 인증 코드와 함께 클라이언트 아이디 및 리디렉션 URL이 포함됩니다.
    4. kakao_token = requests.post(...): 구성된 데이터를 사용하여 카카오에 인증 요청을 보냅니다. 이를 통해 액세스 토큰을 얻습니다.
    5. access_token = kakao_token.json().get("access_token"): 받은 응답에서 액세스 토큰을 추출합니다.
    6. user_data = requests.get(...): 액세스 토큰을 사용하여 카카오 사용자 정보를 얻기 위해 요청을 보냅니다.
    7. user_data = user_data.json(): 받은 사용자 정보를 JSON 형식으로 변환합니다.
    8. data = { ... }: 카카오에서 받은 사용자 정보를 가공하여 저장할 데이터를 구성합니다.
    9. return social_login_validate(**data): 위에서 구성한 데이터를 이용하여 social_login_validate 함수를 호출하고, 그 결과를 반환합니다.
    '''
    def get(self, request):
        return Response(settings.KK_API_KEY, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # with transaction.atomic():
            auth_code = request.data.get("code")
            kakao_token_api = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": settings.KK_API_KEY,
                "redirect_uri": "https://keykey.vercel.app/auth", # 리다이렉트 링크는 배포 링크에 맞춰 수정
                "code": auth_code,
            }
            kakao_token = requests.post(
                kakao_token_api,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data,
            )
            access_token = kakao_token.json().get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            )
            user_data = user_data.json()
            # data 파라미터는 프론트엔드에서 설정
            login_data = {
                "photo": user_data.get("properties").get("profile_image"),
                "username": user_data.get("kakao_account").get("account_email"),
                "nickname": user_data.get("properties").get("profile_nickname"),
                "login_type": "kakao",
                "is_active": True,
            }
            return social_login_validate(**login_data)
        except Exception:
            return Response({"error": "로그인 실패!"}, status=status.HTTP_400_BAD_REQUEST)



class GoogleLoginView(APIView):
    def get(self, request):
        return Response(settings.GC_ID, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # with transaction.atomic():
            access_token = request.data["access_token"]
            if access_token is None:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user_data = requests.get(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            user_data = user_data.json()
            login_data = {
                "username": user_data.get("email"),
                "nickname": user_data.get("name"),
                "photo": user_data.get("picture"),
                "login_type": "google",
                "is_active": True,
            }
            return social_login_validate(**login_data)
        except Exception:
            return Response({"error": "로그인 실패!"}, status=status.HTTP_400_BAD_REQUEST)


def social_login_validate(**kwargs):
    """
    통합 소셜 로그인 함수
    DB에 계정 없을 시 자동으로 회원가입 절차 밟음
    """
    data = {k: v for k, v in kwargs.items()}
    username = data.get("username")
    login_type = data.get("login_type")
    if not username:
        return Response(
            {"error": "해당 계정에 email정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = CustomUser.objects.get(username=username)
        if login_type == user.login_type:
            refresh = RefreshToken.for_user(user)
            access_token = serializers.CustomTokenObtainPairSerializer.get_token(user)
            return Response(
                {"refresh": str(refresh), "access": str(access_token.access_token)},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "같은 이메일로 이미 가입된 계정이 있습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except CustomUser.DoesNotExist:
        return Response(
            {"message": "회원가입 창으로.", "data": data},
            status=status.HTTP_404_NOT_FOUND,
        )
        # new_user = CustomUser.objects.create(**data)
        # new_user.set_unusable_password()
        # new_user.is_active = False
        # new_user.save()
        # refresh = RefreshToken.for_user(new_user)
        # access_token = serializers.CustomTokenObtainPairSerializer.get_token(new_user)
        # return Response(
        #     {"refresh": str(refresh), "access": str(access_token.access_token)},
        #     status=status.HTTP_200_OK,
        # )

class UserView(GenericAPIView, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            access_token = serializers.CustomTokenObtainPairSerializer.get_token(user)

            return Response({"refresh": str(refresh), "access": str(access_token.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfilePhotoUpdateAPIView(generics.UpdateAPIView):
    """
    유저 프로필 사진만 수정
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserProfilePhotoUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailView(APIView):
    '''
    사용자 관련 클래스
    put : 유저 프로필(닉네임, 사진) 수정
    patch : 유저 삭제
    '''
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if request.user.id == user_id:
            serializer = UserDetailSerializer(
                user,
                data=request.data,
                partial=True,
                context={"request": request},
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied

    def patch(self, request, user_id):
        """유저 삭제"""
        user = get_object_or_404(CustomUser, id=user_id)
        if user.login_type == "normal":
            if request.user.id == user_id and user.check_password(
                request.data.get("password")
            ):
                user = request.user
                user.is_active = False
                user.save()
                return Response({"message": "삭제되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "비밀번호가 일치하지 않습니다!"}, status=status.HTTP_403_FORBIDDEN
                )
        else:
            if request.user.id == user_id:
                user = request.user
                user.is_active = False
                user.save()
                return Response({"message": "삭제되었습니다!"}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "권한이 없습니다!"}, status=status.HTTP_403_FORBIDDEN
                )
            

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': '성공적으로 로그아웃되었습니다.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': '유효하지 않거나, 만기된 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)