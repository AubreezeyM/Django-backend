from django.db import models

from users.models import CustomUser

class TextPost(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='Post'
    )
    content = models.TextField(max_length=300)
    post_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

