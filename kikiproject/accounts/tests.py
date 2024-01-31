from django.urls import reverse
from rest_framework.test import APITestCase
from accounts.models import User
from django.utils import timezone

# Create your tests here.
class UserBaseTestCase(APITestCase):
    """유저기능 테스트 준비

    유저기능 테스트를 위한 부모 클래스

    Attribute:
        user: 회원 데이터 추가됨
        user_signup_data: 회원가입을 위한 새로운 유저 데이터(유저1)
        user_edit_data: 회원정보 변경(비밀번호변경)용 데이터(유저2)
        user_login_data: 회원가입한 유저1의 로그인시도 데이터(이메일과비밀번호)
    """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@gmail.com",
            password="xptmxm111!",
        )
        cls.user.is_active = True
        cls.user.save()
        cls.user_signup_data = {
            "username": "testuser2",
            "password": "xptmxm111!",
            "password2": "xptmxm111!",
            "email": "testuser2@gmail.com",
        }
        cls.user_edit_data = {"old_password": "xptmxm111!"}
        cls.user_login_data = {"email": "testuser1@gmail.com", "password": "xptmxm111!"}

    def setUp(self) -> None:
        login_user = self.client.post(
            reverse("custom_token_obtain_pair"), self.user_login_data
        ).data
        self.access = login_user["access"]
        self.refresh = login_user["refresh"]


class UserMultiUserTestCase(UserBaseTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        user_signup_data = {
            "username": "testuser3",
            "password": "xptmxm111!",
            "email": "testuser3@gmail.com",
            # "age": 21,
            # "gender": "female",
        }
        cls.user2 = User.objects.create_user(**user_signup_data)
        cls.user2.is_active = True
        cls.user.save()


class UserSignUpTestCase(UserBaseTestCase):
    """회원가입 테스트

    회원가입을 테스트합니다.
    """

    url = reverse("user_view")

    def test_signup(self):
        """정상: 회원가입

        정상적인 회원가입입
        """
        data = self.user_signup_data
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 201)

        test_signuped_user = User.objects.get(email=data["email"])
        self.assertEqual(test_signuped_user.email, data["email"])

    def test_signup_password_not_same(self):
        """에러: 패스워드 불일치

        패스워드 불일치의 경우입니다.
        """

        data = self.user_signup_data
        data["password2"] = "qhdks222!"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_password_rule(self):
        """에러: 패스워드 규칙위반

        패스워드 규칙을 틀린 경우
        """
        data = self.user_signup_data
        data["password"], data["password2"] = "0000", "0000"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_signup_email_rule(self):
        """에러: 유효하지 않은 email

        이메일 형식이 알맞지 않습니다
        """
        data = self.user_signup_data
        data["email"] = "naver@gmail@gmail.com"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_data(self):
        """에러: 올바르지 않은 age(생년)

        생년이 Date가 아닌경우
        """
        data = self.user_signup_data
        data["age"] = "test"
        response = self.client.post(
            path=self.url,
            data=data,
        )
        self.assertEqual(response.status_code, 400)