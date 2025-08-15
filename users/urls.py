from django.urls import path
from .views import LoginView, CreateUserView, ProfileDetailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail')
]

