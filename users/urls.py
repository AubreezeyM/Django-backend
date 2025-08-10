from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('create/', views.create_user, name='create_user'),
    path('validate/', views.validate_token, name='validate_token'),
    path('all/', views.get_all_users, name='get_all_users'),
]

