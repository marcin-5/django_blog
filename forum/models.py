import uuid
import string

from django.db import models

from home.models import Article
from users.models import CustomUser


def base64uuid():
    res = []
    n = uuid.uuid4().int
    chs = "-_" + string.ascii_lowercase + string.digits + string.ascii_uppercase
    while n:
        res.append(chs[n % 64])
        n //= 64
    return "".join(res) or chs[0]


class Thread(models.Model):
    id = models.CharField(primary_key=True, default=base64uuid, editable=False, max_length=22)
    slug = models.ForeignKey(Article, max_length=50, on_delete=models.CASCADE)
    started_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subject = models.CharField(max_length=200)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.subject} - {self.id}"


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    written_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    text = models.TextField()

    class Meta:
        ordering = ["created"]

    def __str__(self):
        text = self.text.split(".")[0]
        return f"{self.thread.subject} ({self.id}) - {text[:32 if (l := len(text)) > 31 else l]}"
