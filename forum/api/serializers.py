from rest_framework import serializers

from forum.models import Thread, Post


class ThreadsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=22, read_only=True)
    subject = serializers.CharField(max_length=200)
    started_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Thread


class PostsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    written_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    hidden = serializers.BooleanField()
    text = serializers.CharField(trim_whitespace=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = Post
