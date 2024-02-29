from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.UserSignUpPermitView.as_view(),
        name="user_signup_permit",
    ),
    path("api/token/",views.LoginView.as_view(),name="custom_token_obtain_pair",),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("oauth/kakao/", views.KakaoLoginView.as_view(), name="kakao_login"),
    path("oauth/google/", views.GoogleLoginView.as_view(), name="google_login"),
    path("oauth/naver/", views.NaverLoginView.as_view(), name="naver_login"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset/<str:uidb64>/<str:token>/",
        views.UserResetPasswordPermitView.as_view(),
        name="user_reset_password_permit",
    ),
    path("change-password/", views.ChangePasswordView.as_view(), name="change_password"),
    path('photo/update/', views.UserProfilePhotoUpdateAPIView.as_view(), name='update-user-photo'),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('search/program/<int:account_id>/', views.ProSearchView.as_view(), name='pro-search'),
    # path('search/key/<int:account_id>/', views.KeySearchView.as_view(), name='key-search'),
]
