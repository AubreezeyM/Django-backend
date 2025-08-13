from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer, ProfileSerializer
from .models import CustomUser

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = get_object_or_404(CustomUser, username=request.data['username'])
        
        if not user.check_password(request.data['password']):
            return Response(
                {'detail': 'Unauthorized.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
            
        serializer = UserSerializer(instance=user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': serializer.data
        })

class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ValidateTokenView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {'message': f'Test for {request.user.username} passed!'},
            status=status.HTTP_200_OK
        )

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)