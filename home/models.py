import re

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from djongo import models as djongo_models

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


class Content(djongo_models.Model):
    slug = djongo_models.SlugField(blank=True, unique=True, primary_key=True)
    title = djongo_models.CharField(max_length=200)
    text = djongo_models.TextField()

    class Meta:
        ordering = ["title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            pl_chars = dict(
                zip(
                    ("ą", "ć", "ę", "ł", "ń", "ó", "ś", "ż", "ź"),
                    ("a", "c", "e", "l", "n", "o", "s", "z", "z"),
                )
            )
            title = "".join(
                [
                    pl_chars[_] if _ in pl_chars else _
                    for _ in self.title.split(".")[0].lower() or self.title.lower()
                ]
            )
            if not (slug := slugify(title)):
                raise ValidationError("Slug created from title is empty.")
            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Article(models.Model):
    slug = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, blank=True)
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return str(self.slug)
