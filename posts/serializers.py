from rest_framework import serializers
from .models import TextPost

from rest_framework.response import Response

class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = ['id', 'user', 'content', 'post_date', 'modified_date']
        read_only_fields = ['id', 'user', 'post_date', 'modified_date']

    def create(self, validated_data) -> None:
        user = self.context['request'].user
        return TextPost.objects.create(user=user, **validated_data)
    


    