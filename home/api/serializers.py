from rest_framework import serializers

from home.models import Article, Content, Tag, Category


class ArticleSerializer(serializers.Serializer):
    slug = serializers.SlugField(max_length=100, required=True, allow_blank=False)
    is_active = serializers.BooleanField()
    published = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    author = serializers.StringRelatedField(many=False)
    categories = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    title = serializers.StringRelatedField()
    content = serializers.StringRelatedField()

    class Meta:
        model = Article
