from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from forum.api.serializers import ThreadsSerializer, PostsSerializer
from forum.models import Thread, Post


class ThreadListView(generics.ListAPIView):
    serializer_class = ThreadsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Thread.objects.filter(slug=self.kwargs.get("slug"))


class PostListView(generics.ListAPIView):
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(thread=self.kwargs.get("thread"), hidden=True).filter(
            written_by=self.request.user.id
        ) | Post.objects.filter(thread=self.kwargs.get("thread"), hidden=False)


class PostView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(
            thread=self.kwargs.get("thread"), id=self.kwargs.get("pk"), written_by=self.request.user.id
        )


class AddThreadView(generics.CreateAPIView):
    serializer_class = ThreadsSerializer
    permission_classes = [IsAuthenticated]


class AddPostView(generics.CreateAPIView):
    serializer_class = PostsSerializer
    permission_classes = [IsAuthenticated]
