from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='jwt_token'),
    path('token-refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('register/', views.RegistrationView.as_view(), name='user_register'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/<str:user_id>', views.UserDetailView.as_view(), name='user_detail'),
]