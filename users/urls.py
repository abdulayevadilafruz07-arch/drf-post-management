from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    SignUpView,
    LoginView,
    LogoutView,
    UserProfileView,
    UserUpdateView,
    ChangePasswordView
)

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('update/', UserUpdateView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
