from .views import TextPostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('text-posts', TextPostViewSet, basename="posts/")
urlpatterns = router.urls