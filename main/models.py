from django.db import models

from account.models import User


class Post(models.Model):
    author = models.ForeignKey(User, models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
