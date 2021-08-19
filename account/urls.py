from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from account.views import RegisterView, LoginView, UserView, LogoutView, ActivationView, PasswordResetView, CompleteResetPasswordView
 # ActivationView,
    # UserLoginAPIView,  UserLogoutViewAPI

urlpatterns = [
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view()),
    path('password_reset/', PasswordResetView.as_view()),
    path('password_reset_complete/', CompleteResetPasswordView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view(), name='activate'),
]