from django.urls import path
from .views import *
from .views import SendOtp,RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('api/login/', MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('api/admin_login/',MyAdminTokenObtainPairView.as_view(), name="admin_token_obtain_pair"),
    path('api/login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('api/register/',RegisterView.as_view(),name="sign_up"),
    path('api/initiate-verify/',InitiateVerificationView.as_view(), name = "initiate-verify"),
    path('api/verify-user/',VerifyUserView.as_view(),name='verify-user'),
    path('api/sent-otp-partner/', SentOtpForPartnerLogin.as_view(), name='sent-otp-partner'),
    path('api/verify-partner-login-otp/',VerifyPartnerLoginOtpView.as_view(),name='verify-partner-login-otp'),
]
