import uuid

from django.db import models

from home.models import Article
from users.models import CustomUser


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, max_length=8)
    slug = models.OneToOneField(Article, max_length=50, on_delete=models.CASCADE)
    started_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=200)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.subject


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        ordering = ["created"]
