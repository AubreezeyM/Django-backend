from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from .models import CustomUser

@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response(
            {'detail': 'User not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = UserSerializer(instance=user)
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': serializer.data
    })

@api_view(['POST'])
def create_user(request):
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

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def validate_token(request):
    return Response(
        {'message': f'Test for {request.user.username} passed!'},
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_all_users(request):
    return Response({'message': 'get_all_users() reached!'})


