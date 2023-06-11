from rest_framework import serializers

from forum.models import Thread, Post
from home.models import Article


class ThreadsSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=22, read_only=True)
    subject = serializers.CharField(max_length=200)
    started_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Thread

    def create(self, validated_data):
        validated_data["slug"] = Article.objects.get(slug=self.context["view"].kwargs["slug"])
        validated_data["started_by"] = self.context["view"].request.user
        return Thread.objects.create(**validated_data)


class PostsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    written_by = serializers.SlugRelatedField(many=False, read_only=True, slug_field="id")
    created = serializers.DateTimeField(read_only=True)
    updated = serializers.DateTimeField(read_only=True)
    hidden = serializers.BooleanField()
    text = serializers.CharField(trim_whitespace=False, style={'base_template': 'textarea.html'})

    class Meta:
        model = Post

    def create(self, validated_data):
        validated_data["thread"] = Thread.objects.get(pk=self.context["view"].kwargs["thread"])
        validated_data["written_by"] = self.context["view"].request.user
        return Post.objects.create(**validated_data)
