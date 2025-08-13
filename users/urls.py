from django.urls import path
from .views import LoginView, CreateUserView, ValidateTokenView, ProfileDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('validate/', ValidateTokenView.as_view(), name='validate_token'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail')
]

