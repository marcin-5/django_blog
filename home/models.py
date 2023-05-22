import re

from django.db import models
from django.utils.text import slugify

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = re.sub(r"[^a-zA-Z0-9]", "", self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.name}"


class Category(models.Model):
    name = models.CharField(max_length=32, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, unique=True)
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title
