from rest_framework import serializers
from .models import CustomUser, Profile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomObtainTokensSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        data['username'] = self.user.username
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'bio', 'birth_date']
        read_only_fields = ['user']