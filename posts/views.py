from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import TextPostSerializer
from .models import TextPost

class TextPostViewSet(ModelViewSet):
    queryset = TextPost.objects.all()
    serializer_class = TextPostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request):
        serializer = TextPostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            serializer.save(user=self.request.user)
            return Response(post.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    