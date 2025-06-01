from django.urls import path
from accounts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
urlpatterns = [
    # path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('get-session/', GetSessionView.as_view(), name='get_session'),
    path('update-user-data/', UpdateUserDataView.as_view(), name='update_user_data'),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]