from django.http import JsonResponse
from rest_framework import generics

from home.api.serializers import ArticleSerializer
from home.models import Article


def hello_world(request):
    return JsonResponse(data={"message": "Hello World!"})


class ArticleView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug"
