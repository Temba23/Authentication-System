from django.urls import path, include
from .views import RegisterUserAPIView, UserDetailAPI, LoginAPIView, LogoutAPIView, VerifyAPIView, SecurityQuestionAPIView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # path('rest/', include('rest_framework.urls')),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('verify/', VerifyAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('register/', RegisterUserAPIView.as_view(), name="register"), 
    path('me/', UserDetailAPI.as_view(), name="user-detail"),
    

    # JWT
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    # Security Questions
    path('security/', SecurityQuestionAPIView.as_view(), name="security_questions"),
]