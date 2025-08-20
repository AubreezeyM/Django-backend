from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomObtainTokensSerializer

class CustomObtainTokensView(TokenObtainPairView):
    serializer_class = CustomObtainTokensSerializer