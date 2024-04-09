from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


"""유저 모델

    AbstractUser 유저 모델을 커스텀한 유저 모델입니다.

    Attributes:
        LoginTypeChoices(class) : 회원가입 유형(일반,카카오,구글,네이버)
        email (str): 이메일, 필수
        username (str) : 닉네임, 필수
        password (str): 패스워드, 필수
        photo(str) : 유저의 프로필 사진을 url로 가져옵니다.
        updated_at (date): 수정시간
        created_at (date): 가입시간
        login_type (str): 회원가입 유형의 종류를 지정
        is_active (bool): 활성 여부
        is_admin (bool): 관리자 여부
        is_host(bool): 본인 여부
    """
class CustomUser(AbstractUser):
    class LoginTypeChoices(models.TextChoices):
        KAKAO = ("kakao", "카카오")
        GOOGLE = ("google", "구글")
    class OSTypechoices(models.TextChoices):
        WINDOWS = ("windows", "윈도우")
        MAC = ("mac", "맥")
    class JobTypeChoices(models.TextChoices):
        PRODUCER = ("producer", "기획자")
        DESIGNER = ("designer", "디자이너")
        DEVELOPER = ("developer", "개발자")
        OTHERS = ("others", "기타")
    class YearTypeChoices(models.TextChoices):
        UNDERONE = ("underone", "1년 미만")
        ONETOTHREE = ("onetothree", "1년~3년")
        THREETOFIVE = ("threetofive", "3년~5년")
        ABOVEFIVE = ("abovefive", "5년 이상")
        STARTER = ("starter", "취준생")
    username =models.CharField(
        max_length=255,
        unique=True,
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
    )
    nickname = models.CharField(
        max_length=10,
        default='Default nickname',
    )
    password = models.CharField(max_length=256)
    photo = models.ImageField(upload_to='user_photos/', default='user_photos/default.png')
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    login_type = models.CharField(
        max_length=15,
        choices=LoginTypeChoices.choices,
    )
    os_type = models.CharField(
        max_length=15,
        choices=OSTypechoices.choices,
    )
    job_type = models.CharField(
        max_length=15,
        choices=JobTypeChoices.choices,
        default="OTHERS",
    )
    year_type = models.CharField(
        max_length=15,
        choices=YearTypeChoices.choices,
        default="STARTER"
    )
    is_active = models.BooleanField(
        default=True,
    )
    is_admin = models.BooleanField(
        default=False,
    )
    bookmark_program = models.TextField(blank=True)
    bookmark_shortcut = models.TextField(blank=True)
    # is_host = models.BooleanField(
    #     default=False,
    # )

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name_plural = "Users"