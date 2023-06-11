from rest_framework import serializers

from forum.models import Thread, Post


class ThreadsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=22)
    subject = serializers.CharField(max_length=200)
    started_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Thread


class PostsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    written_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    hidden = serializers.BooleanField()
    text = serializers.CharField()

    class Meta:
        model = Post
