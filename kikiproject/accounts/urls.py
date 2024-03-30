from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("", views.UserView.as_view(), name="user_view"),
    path("api/token/",views.LoginView.as_view(),name="custom_token_obtain_pair",),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("oauth/google/", views.GoogleLoginView.as_view(), name="google_login"),
    path('photo/update/', views.UserProfilePhotoUpdateAPIView.as_view(), name='update-user-photo'),
    path("<int:user_id>/", views.UserDetailView.as_view(), name="user_detail"),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
