from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'profile', views.ProfileViewSet, basename='profile')

urlpatterns = router.urls

